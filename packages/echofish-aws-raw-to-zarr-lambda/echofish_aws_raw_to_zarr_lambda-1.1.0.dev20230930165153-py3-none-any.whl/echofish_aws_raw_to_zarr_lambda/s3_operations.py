# s3_operations.py

import os
import boto3
from collections.abc import Generator
from botocore.config import Config
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

MAX_POOL_CONNECTIONS = 64
MAX_CONCURRENCY = 64
MAX_WORKERS = 64


class S3Operations:
    #####################################################################
    def get_client(
            self,
            access_key_id=None,
            secret_access_key=None
    ):
        client_config = Config(max_pool_connections=MAX_POOL_CONNECTIONS)
        session = boto3.Session()
        if access_key_id and secret_access_key:
            # Usually this will indicate an interaction with the NODD bucket
            # or a bucket that is supposed to mimic it as the output bucket
            s3_client = session.client(
                service_name='s3',
                config=client_config,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
            )
        else:
            # Usually this will indicate a bucket created by the stack
            # typically an input bucket
            s3_client = session.client(
                service_name='s3',
                config=client_config,
            )
        return s3_client

    #####################################################################
    def chunked(
            self,
            ll: list,
            n: int
    ) -> Generator:
        """Yields successively n-sized chunks from ll.

        Parameters
        ----------
        ll : list
            List of all objects.
        n : int
            Chunk size to break larger list down from.

        Returns
        -------
        Batches : Generator
            Breaks the data into smaller chunks for processing
        """
        for i in range(0, len(ll), n):
            yield ll[i:i + n]

    #####################################################################
    def list_objects(  # analog to "find_children_objects"
            self,
            bucket_name,
            prefix,
            access_key_id=None,
            secret_access_key=None
    ):
        # Returns a list of key strings for each object in bucket defined by prefix
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        keys = []
        for page in s3_client.get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=prefix):
            if 'Contents' in page.keys():
                keys.extend([k['Key'] for k in page['Contents']])
        return keys

    #####################################################################
    def download_file(
            self,
            bucket_name,
            key,
            file_name,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        s3_client.download_file(Bucket=bucket_name, Key=key, Filename=file_name)
        print('downloaded file')

    #####################################################################
    def delete_object(
            self,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        s3_client.delete_object(Bucket=bucket_name, Key=key)

    #####################################################################
    def __paginate_child_objects(
            self,
            bucket_name: str,
            sub_prefix: str = None,
            access_key_id: str = None,
            secret_access_key: str = None,
    ) -> list:
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        page_iterator = s3_client.get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=sub_prefix)
        objects = []
        for page in page_iterator:
            if 'Contents' in page.keys():
                objects.extend(page['Contents'])
        return objects

    #####################################################################
    def get_child_objects(
            self,
            bucket_name: str,
            sub_prefix: str,
            file_suffix: str = None,
            access_key_id: str = None,
            secret_access_key: str = None,
    ) -> list:
        print('Getting child objects')
        raw_files = []
        try:
            children = self.__paginate_child_objects(
                bucket_name=bucket_name,
                sub_prefix=sub_prefix,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key
            )
            if file_suffix is None:
                raw_files = children
            else:
                for child in children:
                    # Note any files with predicate 'NOISE' are to be ignored, see: "Bell_M._Shimada/SH1507"
                    # cruise for more details.
                    if child['Key'].endswith(file_suffix) and not os.path.basename(child['Key']).startswith(('NOISE')):
                        raw_files.append(child['Key'])
                return raw_files
        except ClientError as err:
            print(f"Problem was encountered while getting s3 files: {err}")
            raise
        print(f"Found {len(raw_files)} files.")
        return raw_files

    #####################################################################
    def delete_objects(
            self,
            bucket_name: str,
            objects: list,
            access_key_id: str = None,
            secret_access_key: str = None
    ):
        print(f"Deleting {len(objects)} objects in {bucket_name} in batches.")
        s3_client = self.get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        objects_to_delete = []
        for object in objects:
            objects_to_delete.append({'Key': object})
        # Delete in groups of 100 -- a Boto3 constraint
        for batch in self.chunked(objects_to_delete, 1000):
            deleted = s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": batch}
            )
            print(f"Deleted {len(deleted['Deleted'])} files")

    #####################################################################
    def upload_file(
            self,
            file_name,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        s3_client.upload_file(
            Filename=file_name,
            Bucket=bucket_name,
            Key=key,
            Config=TransferConfig(
                max_concurrency=MAX_CONCURRENCY,
                use_threads=True,
                max_bandwidth=None,
            ),
        )
        return key

    #####################################################################
    def upload_files_with_thread_pool_executor(
            self,
            bucket_name: str,
            all_files: list,  # is passed a list of lists: [[local_path, s3_key], [...], ...]
            access_key_id: str = None,
            secret_access_key: str = None
    ):
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        all_uploads = []
        try:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [executor.submit(
                    s3_client.upload_file,
                    all_file[0],            # file_name
                    bucket_name,            # bucket_name
                    all_file[1]             # key
                ) for all_file in all_files]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        all_uploads.extend(result)
        except Exception as err:
            print(err)
        print('Done uploading files using threading pool.')
        return all_uploads

    #####################################################################
    def head_object(
            self,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_object.html#S3.Client.head_object
        response = s3_client.head_object(
            Bucket=bucket_name,
            Key=key,
        )

    #####################################################################
    #####################################################################
