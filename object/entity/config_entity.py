import os
from dataclasses import dataclass
from typing import List, Tuple
from object.constant import *
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class TrainingPipelineConfig: 
    artifacts_dir: str = os.path.join(ARTIFACTS_DIR,TIMESTAMP)


training_pipeline_config : TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir : str = os.path.join(
        training_pipeline_config.artifacts_dir,DATA_INGESTION_DIR_NAME    )
    feature_store_file_path: str = os.path.join(
        data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR
    )
    S3_DATA_NAME = DATA_INGESTION_S3_DATA_NAME
    S3_DATA_BUCKET = DATA_INGESTION_S3_BUCKET_NAME



@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_VALIDATION_DIR_NAME
    )
    valid_status_file_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)
    required_file_list = DATA_VALIDATION_REQUIRED_FILES

@dataclass
class ModelTrainerConfig:
    model_trainer_dir:str =os.path.join(training_pipeline_config.artifacts_dir,MODEL_TRAINER_DIR
    )
    model_weights_url :str =MODEL_TRAINER_PRETRAINED_WEIGHTS_URL
    model_epochs :str = MODEL_TRAINER_EPOCHS
    model_batch_size :str = MODEL_TRAINER_BATCH_SIZE

@dataclass
class ModelPusherConfig:
    model_bucket_name:str = MODEL_S3_BUCKET_NAME
    s3_key:str = S3_MODEL_NAME