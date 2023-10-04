#!/usr/bin/env python3

import json
import os
import pathlib
import pickle
import pandas as pd
import re
import requests
import yaml

from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from markdown import markdown as markdown_reader
from pypdf import PdfReader as pdf_reader
from pyth.plugins.rtf15.reader import Rtf15Reader as rtf_reader
from typing import Union, List

from cortex_cli.cli.cli_multipart_upload import MultipartUpload


class CortexFile(namedtuple('BaseFile', 'local_dir remote_path size etag last_modified')):
    _loaded_data = None

    @property
    def local_path(self):
        return '{}/{}'.format(self.local_dir, self.remote_path)


    @property
    def name(self):
        # File name with file extension
        return os.path.basename(self.remote_path)


    @property
    def type(self):
        return pathlib.Path(self.remote_path).suffix.lower().replace('.', '')


    @property
    def loaded_data(self):
        return self._loaded_data


    @property
    def isPandasLoadable(self):
        return self.type in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'csv']


    def load(self, as_polars: bool=False):
        if as_polars:
            try:
                import polars as pl
            except ImportError:
                raise Exception('Polars library is not installed. Please install it using "pip install polars"')
        try:
            # Process doc and docx filetypes
            if self.type in ['doc', 'docx']:
                if self.type=='doc':
                    from doc import Document
                if self.type=='docx':
                    from docx import Document
                
                document = Document(self.local_path)
                paragraphs = [paragraph.text for paragraph in document.paragraphs]
                combined_text = ' '.join(paragraphs)
                self._loaded_data = combined_text
            else:
            
                # Process all other filetypes
                with open(self.local_path, 'rb') as file:
                    if self.type in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']:
                        if as_polars:
                            self._loaded_data = pl.read_excel(file)
                        else:
                            self._loaded_data = pd.read_excel(file)

                    if self.type=='csv':
                        if as_polars:
                            self._loaded_data = pl.read_csv(file)
                        else:
                            self._loaded_data = pd.read_csv(file)

                    if self.type=='json':
                        self._loaded_data = json.load(file)

                    if self.type=='md':
                        text = file.read()
                        html = markdown_reader(text)
                        plain_text = re.sub('<[^<]+?>', '', html)

                        self._loaded_data = plain_text

                    if self.type=='parquet':
                        if as_polars:
                            self._loaded_data = pl.read_parquet(file)
                        else:
                            self._loaded_data = pd.read_parquet(file)

                    if self.type=='pdf':
                        reader = pdf_reader(file)
                        num_pages = reader.pages

                        text = ''
                        for page in reader.pages:
                            text += page.extract_text()
                        
                        self._loaded_data = text
                        
                    if self.type=='pkl':
                        self._loaded_data = pickle.load(file)
                    
                    if self.type=='rtf':
                        doc = rtf_reader.read(file)
                        text = ''
                        for paragraph in doc.content:
                            text += paragraph.plain_text()
                        
                        self._loaded_data = text
                        
                    if self.type=='txt':
                        self._loaded_data = file.read().decode('utf-8')

                    if self.type=='yml':
                        self._loaded_data = yaml.load(file)
                    
            return self._loaded_data
        except IOError:
            # Throw an exception if there is an unsupported file type
            raise Exception('File {} could not be opened by Cortex File'.format(self.name))
    
    
    def exists(self):
        return os.path.isfile(self.local_path)


class CortexData():
    _api_url = None
    _headers = None
    _local_dir = None
    _files = []


    @property
    def files(self):
        return self._files


    def __init__(self, model_id, api_url, headers, local_dir='data/'):
        self._model_id = model_id
        self._api_url = api_url
        self._headers = headers
        self._local_dir = local_dir

        self._files = self._list_remote_files()


    def _list_remote_files(self):
        response = requests.get(
            f'{self._api_url}/models/{self._model_id}/files',
            headers=self._headers
        ).json()

        return [CortexFile(self._local_dir, file['key'], file['size'], file['etag'], file['lastModified'])
                for file in response['documents']]


    def download_files(self, batch_size: int=1, max_workers: int=None):
        # Return if there are no files to download
        if len(self._files) == 0:
            return

        # List all remote files
        self._files = self._list_remote_files()

        batch_results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(0, len(self._files), batch_size):
                batch_input = self._files[i: i + batch_size]
                batch_results.append(executor.submit(self._batch_download_files, batch_input, batch_size, i))
            for result in as_completed(batch_results):
                result.result()


    def _batch_download_files(self, batch, batch_size, batch_idx):
        for i in range(len(batch)):
            download_url = requests.post(
                f'{self._api_url}/models/{self._model_id}/files/download',
                headers=self._headers,
                json={'key': batch[i].remote_path}
            ).json()['url']

            # TODO: Handle api errors

            file_name = batch[i].name
            local_path = batch[i].local_path

            if local_path != (self._local_dir + '/') and not self.find_file(file_name).exists():
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                # Write file to local directory
                with open(local_path, "wb") as binary_file:
                    # Initiate file download
                    file_download = requests.get(
                        download_url
                    )
                    # Write bytes to file
                    binary_file.write(file_download.content)


    def upload_to_cortex(self, file_paths: Union[str, List[str]]):
        # Convert single file to list format
        if not isinstance(file_paths, list):
            file_paths = [file_paths]

        uploadable_files = []

        # Obtain CortexFile objects for all file paths
        for i in range(len(file_paths)):
            # Fix for data directory
            local_dir = self._local_dir
            if file_paths[i].startswith(local_dir):
                file_paths[i] = file_paths[i][len(local_dir):]
            else:
                local_dir = os.dirname(file_paths[i])

            uploadable_file = CortexFile(local_dir, file_paths[i], None, None, None)

            # Overwrite uploadable_file with CortexFile if it already exists in Cortex
            for f in self._files:
                if f.remote_path == file_paths[i]:
                    uploadable_file = f
                    break
            uploadable_files.append(uploadable_file)

        # Sync all files to Cortex
        self.sync_to_cortex(uploadable_files)


    def sync_to_cortex(self, files: Union[CortexFile, List[CortexFile]]):
        # Convert single file to list format
        if not isinstance(files, list):
            files = [files]

        # Syncs files to S3
        remote_paths = [f.remote_path for f in files]
        # TODO: Multithread upload
        for i in range(len(remote_paths)):
            # Fix for data directory
            remote_path = remote_paths[i] if files[i].local_dir == self._local_dir else files[i].local_dir + remote_paths[i]

            uploadable_file = MultipartUpload(
                local_path = files[i].local_path,
                remote_path = remote_path,
                endpoint = f'{self._api_url}/models/{self._model_id}/files',
                headers = self._headers,
                use_path=True
            )
            
            uploadable_file.upload()

            # TODO: Optionally add CortexFile if file doesn't exist in self._files


    def find_file(self, name: str):
        # Find file with name
        for file in self._files:
            if file.name == name:
                return file
        raise FileNotFoundError(f'File {name} not found in Cortex data.')
