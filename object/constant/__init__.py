ARTIFACTS_DIR: str = "artifacts"

"""DATA INGESTION RELEATED CONSTANTS"""

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_S3_DATA_NAME: str = "RoboflowImages.zip"
DATA_INGESTION_S3_BUCKET_NAME: str = "mlops-object-data"

"""DATA validation realated Constants"""
DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_STATUS_FILE = "status.txt"
DATA_VALIDATION_REQUIRED_FILES = ["images", "labels",  "train.txt", "val.txt"]

"""MODEL TRAINER RELATED CONSTANTS"""
MODEL_TRAINER_DIR:str = "model_trainer"  
MODEL_TRAINER_PRETRAINED_WEIGHTS_URL:str = "https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt"
MODEL_TRAINER_EPOCHS: int = 1
MODEL_TRAINER_BATCH_SIZE: int = 8

"""MODEL PUSHER RELATED CONSTANTS"""
MODEL_S3_BUCKET_NAME :str = "mlops-object-data"
S3_MODEL_NAME: str ="best.pt"