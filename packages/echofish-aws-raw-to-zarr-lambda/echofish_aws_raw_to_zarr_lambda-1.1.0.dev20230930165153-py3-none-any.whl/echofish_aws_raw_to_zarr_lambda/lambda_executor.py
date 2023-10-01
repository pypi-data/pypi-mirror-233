# lambda_executor.py
import os
import gc
import glob
import json
import shutil
import geopandas
import numcodecs
import numpy as np
import pandas as pd
import echopype as ep
from datetime import datetime

numcodecs.blosc.use_threads = False


TEMPDIR = "/tmp"

class LambdaExecutor:

    ############################################################################
    def __init__(
            self,
            s3_operations,
            dynamo_operations,
            sns_operations,
            input_bucket,
            output_bucket,
            table_name,
            output_bucket_access_key,
            output_bucket_secret_access_key,
            done_topic_arn,
            # overwrite_existing_zarr_store,
    ):
        self.__s3 = s3_operations
        self.__dynamo = dynamo_operations
        self.__sns_operations = sns_operations
        self.__input_bucket = input_bucket
        self.__output_bucket = output_bucket
        self.__table_name = table_name
        self.__output_bucket_access_key = output_bucket_access_key
        self.__output_bucket_secret_access_key = output_bucket_secret_access_key
        self.__done_topic_arn = done_topic_arn
        # self.__overwrite_existing_zarr_store = overwrite_existing_zarr_store

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
    def __zarr_info_to_table(
            self,
            file_name,
            cruise_name,
            zarr_path,
            min_echo_range,
            max_echo_range,
            num_ping_time_dropna,
            start_time,
            end_time,
            frequencies,
            channels
    ):
        print('Writing Zarr information to DynamoDB table.')
        self.__dynamo.update_item(
            table_name=self.__table_name,
            key={
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
                # TODO: should be FILE_NAME & SENSOR_NAME so they are truely unique for when two sensors are processed within one cruise
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
    def __update_processing_status(
            self,
            file_name: str,
            cruise_name: str,
            pipeline_status: str,
            error_message: str = None,
    ):
        print(f"Updating processing status to {pipeline_status}.")
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

    ############################################################################
    def __get_gps_data(
            self,
            echodata: ep.echodata.echodata.EchoData
    ) -> tuple:
        print('Getting GPS data.')
        try:
            # if 'latitude' not in echodata.platform.variables and 'longitude' not in echodata.platform.variables:
            #     raise KeyError;
            assert(  # TODO: raise error, e.g. KeyError
                    'latitude' in echodata.platform.variables and 'longitude' in echodata.platform.variables
            ), "Problem: GPS coordinates not found in echodata."
            latitude = echodata.platform.latitude.values
            longitude = echodata.platform.longitude.values  # len(longitude) == 14691
            # RE: time coordinates: https://github.com/OSOceanAcoustics/echopype/issues/656#issue-1219104771
            assert(
                    'time1' in echodata.platform.variables and 'time1' in echodata.environment.variables
            ), "Problem: Time coordinate not found in echodata."
            # 'nmea_times' are times from the nmea datalogger associated with GPS
            #   nmea times, unlike env times, can be sorted
            nmea_times = np.sort(echodata.platform.time1.values)
            # 'time1' are times from the echosounder associated with transducer measurement
            time1 = echodata.environment.time1.values
            # Align 'sv_times' to 'nmea_times'
            assert(
                    np.all(time1[:-1] <= time1[1:]) and np.all(nmea_times[:-1] <= nmea_times[1:])
            ), "Problem: NMEA time stamps are not sorted."
            # Finds the indices where 'v' can be inserted just to the right of 'a'
            indices = np.searchsorted(a=nmea_times, v=time1, side="right") - 1
            #
            lat = latitude[indices]
            lat[indices < 0] = np.nan  # values recorded before indexing are set to nan
            lon = longitude[indices]
            lon[indices < 0] = np.nan
            if len(lat) < 2 or len(lon) < 2:
                raise Exception("There was not enough data in lat or lon to create geojson.")
            assert(  # TODO: raise ValueError
                    np.all(lat[~np.isnan(lat)] >= -90.) and np.all(lat[~np.isnan(lat)] <= 90.) and np.all(lon[~np.isnan(lon)] >= -180.) and np.all(lon[~np.isnan(lon)] <= 180.)
            ), "Problem: Data falls outside GPS bounds!"
            # TODO: check for visits to null island
            # https://osoceanacoustics.github.io/echopype-examples/echopype_tour.html
            print(np.count_nonzero(np.isnan(lat)))
            print(np.count_nonzero(np.isnan(lon)))
            if len(lat[~np.isnan(lat)]) < 1:
                raise RuntimeError(f"Problem all data is NaN.")
            time1 = time1[~np.isnan(lat)]
            lat = lat[~np.isnan(lat)]
            lon = lon[~np.isnan(lon)]
            #
            gps_df = pd.DataFrame({
                'latitude': lat,
                'longitude': lon,
                'time1': time1
            }).set_index(['time1'])
            gps_gdf = geopandas.GeoDataFrame(
                gps_df,
                geometry=geopandas.points_from_xy(gps_df['longitude'], gps_df['latitude']),
                crs="epsg:4326"  # TODO: does this sound right?
            )
            # GeoJSON FeatureCollection with IDs as "time1"
            geo_json = gps_gdf.to_json()
        except Exception as err:
            print(f'Exception encountered creating local Zarr store with echopype: {err}')
            raise
        return geo_json, lat, lon

    ############################################################################
    def __write_geojson_to_file(
            self,
            store_name,
            data
    ) -> None:
        print('Writing GeoJSON to file.')
        with open(os.path.join(store_name, 'geo.json'), "w") as outfile:
            outfile.write(data)

    ############################################################################
    def __create_local_zarr_store(
            self,
            raw_file_name,
            cruise_name,
            sensor_name,
            output_zarr_prefix,
            store_name
    ):
        print(f'Opening raw: {raw_file_name} and creating local zarr store.')
        try:
            gc.collect()
            print('Opening raw file with echopype.')  # TODO: next idea is use garbage collector...
            echodata = ep.open_raw(raw_file_name, sonar_model=sensor_name, use_swap=True, max_mb=100)  # use_swap=True
            print('Compute volume backscattering strength (Sv) from raw data.')
            ds_sv = ep.calibrate.compute_Sv(echodata)
            print('Done computing volume backscattering strength (Sv) from raw data.')
            frequencies = echodata.environment.frequency_nominal.values
            #################################################################
            # Get GPS coordinates
            gps_data, lat, lon = self.__get_gps_data(echodata=echodata)
            #################################################################
            # Technically the min_echo_range would be 0 m.
            # TODO: this var name is supposed to represent minimum resolution of depth measurements
            # The most minimum the resolution can be is as small as 0.25 meters
            min_echo_range = np.maximum(0.25, np.nanmin(np.diff(ds_sv.echo_range.values)))
            max_echo_range = float(np.nanmax(ds_sv.echo_range))
            #
            num_ping_time_dropna = lat[~np.isnan(lat)].shape[0]  # symmetric to lon
            #
            start_time = np.datetime_as_string(ds_sv.ping_time.values[0], unit='ms') + "Z"
            end_time = np.datetime_as_string(ds_sv.ping_time.values[-1], unit='ms') + "Z"
            channels = list(ds_sv.channel.values)
            #
            #################################################################
            # Create the zarr store
            ds_sv.to_zarr(store=store_name)
            #################################################################
            print('Note: Adding GeoJSON inside Zarr store')
            self.__write_geojson_to_file(store_name=store_name, data=gps_data)
            #################################################################
            self.__zarr_info_to_table(
                file_name=raw_file_name,
                cruise_name=cruise_name,
                zarr_path=os.path.join(output_zarr_prefix, store_name),
                min_echo_range=min_echo_range,
                max_echo_range=max_echo_range,
                num_ping_time_dropna=num_ping_time_dropna,
                start_time=start_time,
                end_time=end_time,
                frequencies=frequencies,
                channels=channels
            )
        except Exception as err:
            print(f'Exception encountered creating local Zarr store with echopype: {err}')
            raise RuntimeError(f"Problem creating local Zarr store, {err}")
        print('Done creating local zarr store.')

    ############################################################################
    def __upload_files_to_output_bucket(
            self,
            local_directory,
            object_prefix,
    ):
        # Note: this will be passed credentials if using NODD
        print('Uploading files using thread pool executor.')
        all_files = []
        for subdir, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                s3_key = os.path.join(object_prefix, local_path)
                all_files.append([local_path, s3_key])
        # all_files
        all_uploads = self.__s3.upload_files_with_thread_pool_executor(
            bucket_name=self.__output_bucket,
            all_files=all_files,
            access_key_id=self.__output_bucket_access_key,
            secret_access_key=self.__output_bucket_secret_access_key
        )
        return all_uploads

    ############################################################################
    def __publish_done_message(
            self,
            message
    ):
        print("Sending done message")
        self.__sns_operations.publish(self.__done_topic_arn, json.dumps(message))

    ############################################################################
    def execute(self, input_message):
        ship_name = input_message['shipName']
        cruise_name = input_message['cruiseName']
        sensor_name = input_message['sensorName']
        input_file_name = input_message['fileName']
        #
        try:
            self.__update_processing_status(
                file_name=input_file_name,
                cruise_name=cruise_name,
                pipeline_status="PROCESSING_RAW_TO_ZARR"
            )
            #######################################################################
            store_name = f"{os.path.splitext(input_file_name)[0]}.zarr"
            output_zarr_prefix = f"level_1/{ship_name}/{cruise_name}/{sensor_name}"
            bucket_key = f"data/raw/{ship_name}/{cruise_name}/{sensor_name}/{input_file_name}"
            zarr_prefix = os.path.join("level_1", ship_name, cruise_name, sensor_name)
            #
            os.chdir(TEMPDIR)  # Lambdas require use of temp directory
            #######################################################################
            #######################################################################
            # Check if zarr store already exists
            s3_objects = self.__s3.list_objects(
                bucket_name=self.__output_bucket,
                prefix=f"{zarr_prefix}/{os.path.splitext(input_file_name)[0]}.zarr/",
                access_key_id=self.__output_bucket_access_key,
                secret_access_key=self.__output_bucket_secret_access_key
            )
            if len(s3_objects) > 0:
                print('Zarr store data already exists in s3, deleting existing and continuing.')
                self.__s3.delete_objects(
                    bucket_name=self.__output_bucket,
                    objects=s3_objects,
                    access_key_id=self.__output_bucket_access_key,
                    secret_access_key=self.__output_bucket_secret_access_key
                )
            #######################################################################
            self.__delete_all_local_raw_and_zarr_files()
            self.__s3.download_file(
                bucket_name=self.__input_bucket,
                key=bucket_key,
                file_name=input_file_name
            )
            self.__create_local_zarr_store(
                raw_file_name=input_file_name,
                cruise_name=cruise_name,
                sensor_name=sensor_name,
                output_zarr_prefix=output_zarr_prefix,
                store_name=store_name
            )
            #######################################################################
            self.__upload_files_to_output_bucket(store_name, output_zarr_prefix)
            #######################################################################
            # # TODO: verify count of objects matches
            # s3_objects = self.__s3.list_objects(
            #     bucket_name=self.__output_bucket,
            #     prefix=f"{zarr_prefix}/{os.path.splitext(input_file_name)[0]}.zarr/",
            #     access_key_id=self.__output_bucket_access_key,
            #     secret_access_key=self.__output_bucket_secret_access_key
            # )
            #######################################################################
            self.__update_processing_status(
                file_name=input_file_name,
                cruise_name=cruise_name,
                pipeline_status='SUCCESS_RAW_TO_ZARR'
            )
            #######################################################################
            self.__publish_done_message(input_message)
            #######################################################################
        # except Exception as err:
        #     print(f'Exception encountered: {err}')
            # self.__update_processing_status(
            #     file_name=input_file_name,
            #     cruise_name=cruise_name,
            #     pipeline_status='FAILURE_RAW_TO_ZARR',
            #     error_message=str(err),
            # )
        finally:
            self.__delete_all_local_raw_and_zarr_files()
        #######################################################################
