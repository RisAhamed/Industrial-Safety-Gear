import os
import sys
from object.logger import logging
from pathlib import Path
from six.moves import urllib
import zipfile
import numpy as np
from object.exception import objException
from botocore.exceptions import ClientError
from  object.constant import *
from pandas import DataFrame, read_csv
from object.configuration.s3_operations import S3Operation
from object.entity.artifacts_entity import DataIngestionArtifact
from object.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig,):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.s3 = S3Operation()

        except Exception as e:
            raise objException(e, sys)
        
    def download_data(self)->str:
        try:
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            if not os.path.exists(zip_download_dir):
                os.makedirs(zip_download_dir)
            os.makedirs(zip_download_dir,exist_ok =True)
            logging.info(f"Downloading data from S3 bucket {self.data_ingestion_config.S3_DATA_BUCKET}")
            zipfilepath : Path = os.path.join(zip_download_dir,self.data_ingestion_config.S3_DATA_NAME)
            self.s3.download_object(key = self.data_ingestion_config.S3_DATA_NAME,bucket_name=DATA_INGESTION_S3_BUCKET_NAME,filename=zipfilepath)
            logging.info(f"Dowloading data from s3 bucket is completed" in {zipfilepath})   
            return zipfilepath
        
        except Exception as e:
            raise objException(e, sys)
        
    def extract_zip_file(self,zip_file_path: str) ->str:
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)

            return feature_store_path
        
        except Exception as e:
            raise objException(e,sys)
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        logging.info("started  the data ingestion")
        try:
            zip_file_path =self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path=zip_file_path)
            data_ingestion_artifacts = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,feature_store_path =feature_store_path
            )
            logging.info("data ingestion is completed")
            return data_ingestion_artifacts
        except Exception as e:
            raise objException(e,sys)
        
