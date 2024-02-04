import os
import urllib.request as request
import zipfile
import gzip
import tarfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}") 

    
    def extract_zip_file(self):
        """
        Extracts the gzip-compressed file into the data directory.

        Function returns None.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        
        try:
            with gzip.open(self.config.local_data_file, 'rb') as gz_file:
                with tarfile.open(fileobj=gz_file, mode='r') as tar_ref:
                    tar_ref.extractall(unzip_path)
        except OSError:
            print(f"Error: {self.config.local_data_file} is not a valid gzip-compressed file.")
            # handle the error as needed
