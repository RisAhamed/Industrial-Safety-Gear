import sys
from object.configuration.s3_operations import S3Operation
from object.entity.artifacts_entity import *
from object.entity.config_entity import ModelPusherConfig
from object.exception import objException
from object.logger import logging

class ModelPusher:
    def __init__(self,model_pusher_config: ModelPusherConfig,model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_trainer_artifact = model_trainer_artifact
            self.s3 = S3Operation()
        except Exception as e:
            raise objException(e,sys)
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            logging.info("Entered initiate_model_pusher method of ModelPusher class")
            upload_model = self.s3.upload_file(
                from_filename=self.model_trainer_artifact.trained_model_file_path,
                bucket_name=self.model_pusher_config.model_bucket_name,
                to_filename=self.model_pusher_config.s3_key,remove= False
            )
            logging.info("Uploaded best model to s3 bucket")
            model_pusher_artifact = ModelPusherArtifact(
                model_bucket_name=self.model_pusher_config.model_bucket_name,
                s3_key_path = self.model_pusher_config.s3_key,
            )
            
            logging.info(">>>>>>>>>>>>Exited model_pusher  class<<<<<<<<<<<<<<<<<<")
            return model_pusher_artifact
        except Exception as e:
            raise objException(e,sys)