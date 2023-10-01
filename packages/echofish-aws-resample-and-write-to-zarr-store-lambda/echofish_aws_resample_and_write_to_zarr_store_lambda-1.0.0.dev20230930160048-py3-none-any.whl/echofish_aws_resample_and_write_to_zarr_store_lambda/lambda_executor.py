# lambda_executor.py

import os
import json
import s3fs
import zarr
import glob
import time
# import blosc
import shutil
# from numcodecs import Zstd
import numcodecs
import geopandas
import numpy as np
import xarray as xr
import pandas as pd
from sys import platform
from scipy import interpolate
from datetime import datetime
from botocore.exceptions import ClientError

TEMPDIR = "/tmp"
TILE_SIZE = 512

numcodecs.blosc.use_threads = False  # needed to fix Blosc threaded compression errors
numcodecs.blosc.set_nthreads(1)

class LambdaExecutor:
    ############################################################################
    def __init__(
            self,
            s3_operations,
            s3fs_operations,
            dynamo_operations,
            sns_operations,
            output_bucket,
            table_name,
            output_bucket_access_key,
            output_bucket_secret_access_key,
            done_topic_arn,
    ):
        self.__s3 = s3_operations
        self.__s3fs = s3fs_operations
        self.__dynamo = dynamo_operations
        self.__sns_operations = sns_operations
        self.__output_bucket = output_bucket
        self.__table_name = table_name
        self.__output_bucket_access_key = output_bucket_access_key
        self.__output_bucket_secret_access_key = output_bucket_secret_access_key
        self.__done_topic_arn = done_topic_arn

    ############################################################################
    def __get_processing_status(
            self,
            file_name,
            cruise_name
    ):
        # HASH: FILE_NAME, RANGE: SENSOR_NAME
        item = self.__dynamo.get_item(
            TableName=self.__table_name,
            Key={
                'FILE_NAME': {'S': file_name},      # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            })
        if item is None:
            return 'NONE'
        return item['PIPELINE_STATUS']['S']

    ############################################################################
    def __zarr_info_to_table(
            self,
            cruise_name,
            file_name,
            zarr_path,
            min_echo_range,
            max_echo_range,
            num_ping_time_dropna,
            start_time,
            end_time,
            frequencies,
            channels
    ):
        self.__dynamo.update_item(
            table_name=self.__table_name,
            key={
                'FILE_NAME': {'S': file_name},      # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            },
            expression='SET #ZB = :zb, #ZP = :zp, #MINER = :miner, #MAXER = :maxer, #P = :p, #ST = :st, #ET = :et, #F = :f, #C = :c',
            attribute_names={
                '#ZB': 'ZARR_BUCKET',
                '#ZP': 'ZARR_PATH',
                '#MINER': 'MIN_ECHO_RANGE',
                '#MAXER': 'MAX_ECHO_RANGE',
                '#P': 'NUM_PING_TIME_DROPNA',
                '#ST': 'START_TIME',
                '#ET': 'END_TIME',
                '#F': 'FREQUENCIES',
                '#C': 'CHANNELS',
            },
            attribute_values={
                ':zb': {
                    'S': self.__output_bucket
                },
                ':zp': {
                    'S': zarr_path
                },
                ':miner': {
                    'N': str(np.round(min_echo_range, 4))
                },
                ':maxer': {
                    'N': str(np.round(max_echo_range, 4))
                },
                ':p': {
                    'N': str(num_ping_time_dropna)
                },
                ':st': {
                    'S': start_time
                },
                ':et': {
                    'S': end_time
                },
                ':f': {
                    'L': [{'N': str(i)} for i in frequencies]
                },
                ':c': {
                    'L': [{'S': i} for i in channels]
                }
            }
        )

    ############################################################################
    def __get_table_as_dataframe(
            self,
            ship_name,
            cruise_name,
            sensor_name
    ) -> pd.DataFrame:
        print('get table as dataframe')
        try:
            print(self.__table_name)
            table = self.__dynamo.get_table(table_name=self.__table_name)
            # Note: table.scan() has 1 MB limit on results so pagination is used
            response = table.scan()
            data = response['Items']
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])
            # Filter results when there are other cruises
            df = pd.DataFrame(data)
            df = df[(df['SHIP_NAME'] == ship_name) & (df['CRUISE_NAME'] == cruise_name) & (df['SENSOR_NAME'] == sensor_name)]
        except ClientError as err:
            print('Problem finding the dynamodb table')
            raise err
        return df.sort_values(by='START_TIME', ignore_index=True)

    ############################################################################
    def __get_s3_zarr_as_xr(
            self,
            zarr_path: str
    ) -> xr.core.dataset.Dataset:
        print('getting s3 zarr as xr')
        # The path should be like: f's3://{input_zarr_bucket}/{input_zarr_path}'
        store = self.__s3fs.s3_map(
            s3_zarr_store_path=f"s3://{self.__output_bucket}/{zarr_path}",
            access_key_id=self.__output_bucket_access_key,
            secret_access_key=self.__output_bucket_secret_access_key,
        )
        # You are already using dask, this is assumed by open_zarr, not the same as open_dataset(engine=“zarr”)
        return xr.open_zarr(store=store, consolidated=None)  # synchronizer=SYNCHRONIZER

    ############################################################################
    ############################################################################
    def __interpolate_data(
            self,
            maximum_cruise_depth_meters,  # get from df, type=np.float32
            file_xr: xr.Dataset,  # need to figure out which time values are removed
            cruise_zarr: zarr.Group,
            start_ping_time_index: int,
            end_ping_time_index: int,
            indices: np.ndarray, # the file_xr ping_time and Sv indices that are not np.nan
    ) -> np.ndarray:
        print("Interpolating data.")
        try:
            # Reading remotely once to speed up, fsspec is slow...
            # Note: file_zarr dimensions are (frequency, time, depth)
            num_frequencies = file_xr.channel.shape[0]
            file_sv = file_xr.Sv.values  # (4, 9779, 1302)
            all_file_depth_values = file_xr.echo_range.values[:, :, :]
            # Note: cruise_zarr dimensions are (depth, time, frequency)
            print("Creating empty ndarray for Sv data.")
            cruise_sv_subset = np.empty(shape=cruise_zarr.Sv[:, start_ping_time_index:end_ping_time_index, :].shape)
            cruise_sv_subset[:, :, :] = np.nan  # (5208, 9778, 4)
            # Grid evenly spaced depths over the specified interval
            all_cruise_depth_values = np.linspace(
                start=0,
                stop=np.ceil(maximum_cruise_depth_meters),
                num=cruise_sv_subset.shape[0],
                endpoint=True
            )
            #
            # TODO: need better method for determining the order of the coordinates...
            #
            for iii in range(num_frequencies):
                print(f"Interpolating frequency: {iii}")
                for jjj in range(len(indices)):
                    y = file_sv[indices[jjj], iii, :]  # OLD: y.shape = (4, 4871, 5208) -> frequency, time, depth..... NEW: (9734, 4, 1302) time, channel, depth
                    # all_Sv is only 1302 depth measurements
                    f = interpolate.interp1d(  # Interpolate a 1-D function.
                        x=all_file_depth_values[iii, indices[jjj], :],
                        y=y,  # Need to strip off unwanted timestamps
                        kind='nearest',
                        bounds_error=False,
                        fill_value=np.nan
                    )
                    y_new = f(all_cruise_depth_values)  # y_new.shape = (4, 4871, 5208) --> (frequency, time, depth)
                    # Note: dimensions are (depth, time, frequency)
                    cruise_sv_subset[:, jjj, iii] = y_new  #  .transpose((2, 1, 0))  # (5208, 89911, 4)
            #
        except ClientError as err:
            print('Problem finding the dynamodb table')
            raise err
        print("Done interpolating data.")
        return cruise_sv_subset

    ############################################################################

    def __s3_zarr(
            self,
            output_zarr_bucket: str,
            ship_name: str,
            cruise_name: str,
            sensor_name: str,
            # zarr_synchronizer: Union[str, None] = None,
    ):
        print('Opening s3 Zarr store.')
        try:
            s3 = s3fs.S3FileSystem(
                key=self.__output_bucket_access_key,
                secret=self.__output_bucket_secret_access_key
            )
            root = f'{output_zarr_bucket}/level_2/{ship_name}/{cruise_name}/{sensor_name}/{cruise_name}.zarr'
            store = s3fs.S3Map(root=root, s3=s3)
            # Blosc configuration
            numcodecs.blosc.use_threads = False
            numcodecs.blosc.set_nthreads(1)
            #
            if platform == "linux" or platform == "linux2":
                print('Linux filesystem.')  # in lambda, use mounted /mnt/zarr directory
                if os.path.exists('/mnt/zarr/'):  # if EFS is mounted to lambda, synchronize
                    print('Mount path exists.')
                    print(os.listdir("/mnt/zarr/"))
                    # os.path.getmtime(f"/mnt/zarr/{ship_name}_{cruise_name}.sync")
                    synchronizer = zarr.ProcessSynchronizer(f"/mnt/zarr/{ship_name}_{cruise_name}.sync")
                    # os.path.getmtime(f"/mnt/zarr/{ship_name}_{cruise_name}.sync")
                    # Note: 'r+' means read/write (store must already exist)
                    cruise_zarr = zarr.open(store=store, mode="r+", synchronizer=synchronizer)
                else:
                    print('No /mnt/zarr path found, ignoring synchronization')
                    cruise_zarr = zarr.open(store=store, mode="r+")
            elif platform == "darwin":
                print('Mac filesystem')  # for functional tests, use /tmp directory
                synchronizer = zarr.ProcessSynchronizer(f"/tmp/{ship_name}_{cruise_name}.sync")
                cruise_zarr = zarr.open(store=store, mode="r+", synchronizer=synchronizer)
        except Exception as err:  # Failure
            print(f'Exception encountered: {err}')
            raise
        print('done opening zarr store')
        return cruise_zarr

    ############################################################################
    def __get_spatiotemporal_indices(
            self,
            input_zarr_path: str,
    ) -> tuple:
        try:
            geo_json_s3_path = f's3://{self.__output_bucket}/{input_zarr_path}/geo.json'
            assert(self.__s3fs.exists(
                geo_json_s3_path=geo_json_s3_path,
                access_key_id=self.__output_bucket_access_key,
                secret_access_key=self.__output_bucket_secret_access_key)
            ), "S3 GeoJSON file does not exist."
            geo_json = geopandas.read_file(
                filename=geo_json_s3_path,
                storage_options={
                    "key": self.__output_bucket_access_key,
                    "secret": self.__output_bucket_secret_access_key,
                },
            )
            geo_json.id = pd.to_datetime(geo_json.id)
            geo_json.id.astype('datetime64[ns]')  # TODO: be careful with conversions for pandas >=2.0.0
            epoch_seconds = (
                pd.to_datetime(geo_json.dropna().id, unit='s', origin='unix') - pd.Timestamp('1970-01-01')
            ) / pd.Timedelta('1s')
            epoch_seconds = epoch_seconds.tolist()
            longitude = geo_json.dropna().longitude.tolist()
            latitude = geo_json.dropna().latitude.tolist()
            #
            return latitude, longitude, epoch_seconds
        except Exception as err:  # Failure
            print(f'Exception encountered getting spatial temporal indices: {err}')
            raise

    ############################################################################
    def __read_s3_geo_json(
            self,
            input_zarr_path: str,
    ) -> str:
        try:
            content_object = self.__s3.get_object(bucket_name=self.__output_bucket, input_zarr_path=input_zarr_path)
            print(content_object.get())
            file_content = content_object.get()['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)
            return json_content
        except Exception as err:  # Failure
            print(f'Exception encountered reading s3 GeoJSON: {err}')
            raise

    ############################################################################
    def __update_processing_status(
            self,
            file_name: str,
            cruise_name: str,
            pipeline_status: str,
            error_message: str = None,
    ) -> None:
        print(f"Updating processing status: {pipeline_status}.")
        try:
            if error_message:
                print(f"Error message: {error_message}")
                self.__dynamo.update_item(
                    table_name=self.__table_name,
                    key={
                        'FILE_NAME': {'S': file_name},      # Partition Key
                        'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                    },
                    attribute_names={
                        '#PT': 'PIPELINE_TIME',
                        '#PS': 'PIPELINE_STATUS',
                        '#EM': 'ERROR_MESSAGE',
                    },
                    expression='SET #PT = :pt, #PS = :ps, #EM = :em',
                    attribute_values={
                        ':pt': {
                            'S': datetime.now().isoformat(timespec="seconds") + "Z"
                        },
                        ':ps': {
                            'S': pipeline_status
                        },
                        ':em': {
                            'S': error_message
                        }
                    }
                )
            else:
                self.__dynamo.update_item(
                    table_name=self.__table_name,
                    key={
                        'FILE_NAME': {'S': file_name},      # Partition Key
                        'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                    },
                    attribute_names={
                        '#PT': 'PIPELINE_TIME',
                        '#PS': 'PIPELINE_STATUS',
                    },
                    expression='SET #PT = :pt, #PS = :ps',
                    attribute_values={
                        ':pt': {
                            'S': datetime.now().isoformat(timespec="seconds") + "Z"
                        },
                        ':ps': {
                            'S': pipeline_status
                        }
                    }
                )
            print("Done updating processing status.")
        except Exception as err:  # Failure
            print(f'Exception encountered: {err}')
            raise

    ############################################################################
    def __publish_done_message(
        self,
        message
    ) -> None:
        print("Sending done message")
        self.__sns_operations.publish(self.__done_topic_arn, json.dumps(message))

    ############################################################################
    def __delete_all_local_raw_and_zarr_files(
            self
    ):
        print('Deleting all local raw and zarr files')
        for i in ['*.raw*', '*.zarr']:
            for j in glob.glob(i):
                if os.path.isdir(j):
                    shutil.rmtree(j, ignore_errors=True)
                elif os.path.isfile(j):
                    os.remove(j)
        print('done deleting')

    ############################################################################
    def execute(self, message):
        ship_name = message['shipName']
        cruise_name = message['cruiseName']
        sensor_name = message['sensorName']
        input_file_name = message['fileName']
        #
        try:
            #
            # DELETE THIS!
            #
            # self.__publish_done_message(message)
            #
            #
            self.__update_processing_status(
                file_name=input_file_name,
                cruise_name=cruise_name,
                pipeline_status='PROCESSING_RESAMPLE_AND_WRITE_TO_ZARR_STORE'
            )
            file_stem = os.path.splitext(input_file_name)[0]
            input_zarr_path = f"level_1/{ship_name}/{cruise_name}/{sensor_name}/{file_stem}.zarr"
            print(input_zarr_path)
            #########################################################################
            # AWS Lambda requires work from temp directory
            os.chdir(TEMPDIR)
            #########################################################################
            # [0] get dynamoDB table info
            df = self.__get_table_as_dataframe(ship_name=ship_name, cruise_name=cruise_name, sensor_name=sensor_name)
            # Zarr path is derived from DynamoDB
            ### ZARR_PATH ###
            if input_zarr_path not in list(df['ZARR_PATH']):
                raise Exception(f"Zarr path {input_zarr_path} not found in the database.")
            #
            index = df.index[df['ZARR_PATH'] == input_zarr_path][0]  # index among all cruise files
            #
            file_info = df.iloc[index].to_dict()
            input_zarr_path = file_info['ZARR_PATH']
            output_zarr_bucket = file_info['ZARR_BUCKET']
            #########################################################################
            # [1] read file-level Zarr store using xarray
            geo_json = self.__read_s3_geo_json(input_zarr_path=input_zarr_path)
            file_xr = self.__get_s3_zarr_as_xr(zarr_path=input_zarr_path)
            # {'id': '2007-07-12T15:24:16.032000000', 'type': 'Feature', 'properties': {'latitude': None, 'longitude': None}, 'geometry': None}
            # reads GeoJSON with the id as the index
            geospatial = geopandas.GeoDataFrame.from_features(geo_json['features']).set_index(pd.json_normalize(geo_json["features"])["id"].values)
            geospatial_index = geospatial.dropna().index.values.astype('datetime64[ns]')
            # Finds the indices where 'v' can be inserted into 'a'
            aa = file_xr.ping_time.values.tolist()
            vv = geospatial_index.tolist()
            indices = np.searchsorted(a=aa, v=vv)
            #########################################################################
            # [2] open cruise level zarr store for writing
            cruise_zarr = self.__s3_zarr(
                output_zarr_bucket,
                ship_name,
                cruise_name,
                sensor_name,
            )
            #########################################################################
            # [3] Get needed indices
            # https://github.com/oftfrfbf/watercolumn/blob/8b7ed605d22f446e1d1f3087971c31b83f1b5f4c/scripts/scan_watercolumn_bucket_by_size.py#L138
            # Offset from start index to insert new data. Note that missing values are excluded.
            ping_time_cumsum = np.insert(
                np.cumsum(df['NUM_PING_TIME_DROPNA'].dropna().to_numpy(dtype=int)),
                obj=0,
                values=0
            )
            start_ping_time_index = ping_time_cumsum[index]
            end_ping_time_index = ping_time_cumsum[index + 1]
            #
            #########################################################################
            numcodecs.blosc.use_threads = False
            print(f"nthreads before: {numcodecs.blosc.get_nthreads()}")
            numcodecs.blosc.set_nthreads(1)
            print(f"nthreads after: {numcodecs.blosc.get_nthreads()}")
            #########################################################################
            # [4] extract gps and time coordinate from file-level Zarr store,
            # write subset of ping_time to the larger zarr store
            # reference: https://osoceanacoustics.github.io/echopype-examples/echopype_tour.html
            latitude, longitude, epoch_seconds = self.__get_spatiotemporal_indices(
                input_zarr_path=input_zarr_path
            )
            if len(epoch_seconds) != len(cruise_zarr.time[start_ping_time_index:end_ping_time_index]):
                raise Exception("Number of the timestamps is not equivalent to indices given.")
            cruise_zarr.time[start_ping_time_index:end_ping_time_index] = epoch_seconds
            #########################################################################
            # [5] write subset of latitude/longitude
            cruise_zarr.latitude[start_ping_time_index:end_ping_time_index] = latitude
            cruise_zarr.longitude[start_ping_time_index:end_ping_time_index] = longitude
            #########################################################################
            # [6] get interpolated Sv data
            print('interpolate_data')
            all_sv_prototype = self.__interpolate_data(
                maximum_cruise_depth_meters = np.nanmax(np.float32(df['MAX_ECHO_RANGE'])),
                file_xr=file_xr,
                cruise_zarr=cruise_zarr,
                start_ping_time_index=start_ping_time_index,
                end_ping_time_index=end_ping_time_index,
                indices=indices,
            )
            #########################################################################
            print("Writing all_Sv_prototype data to cruise_zarr.")
            print(f"start_ping_time_index: {start_ping_time_index}")
            print(f"end_ping_time_index: {end_ping_time_index}")
            cruise_zarr.Sv[:, start_ping_time_index:end_ping_time_index, :] = all_sv_prototype
            # print(os.listdir("/mnt/zarr"))
            # if os.path.exists('/mnt/zarr/'):  # if EFS is mounted to lambda, synchronize
            #     print(os.listdir("/mnt/zarr"))
                # os.path.getmtime(f"/mnt/zarr/{ship_name}_{cruise_name}.sync")
            #########################################################################
            # Success
            self.__update_processing_status(
                file_name=input_file_name,
                cruise_name=cruise_name,
                pipeline_status='SUCCESS_RESAMPLE_AND_WRITE_TO_ZARR_STORE'
            )
            self.__publish_done_message(message)
            self.__delete_all_local_raw_and_zarr_files()
        except Exception as err:
            print(f'Exception encountered: {err}')
            self.__update_processing_status(
                file_name=input_file_name,
                cruise_name=cruise_name,
                pipeline_status='FAILURE_RESAMPLE_AND_WRITE_TO_ZARR_STORE',
                error_message=str(err),
            )
        finally:
            # Clean up
            print(f'Done processing {input_file_name}')
