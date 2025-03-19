import sys, os
from  object.logger import logging
from object.exception import objException
from object.configuration.s3_operations import S3Operation
from object.components.data_ingestion import DataIngestion
from object.components.data_validation import DataValidation
from object.components.model_trainer import ModelTrainer
from object.components.model_pusher import ModelPusher
from object.entity.config_entity import *
from object.entity.artifacts_entity import *

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion( self)->DataIngestionArtifact:
        try:
            logging.info(                    "Entered the start_data_ingestion method of TrainPipeline class"                )
            logging.info("Getting the data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config =  self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from URL")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise objException(e, sys)

    def start_data_validation(self,data_ingestion_artifacts)->DataValidationArtifact:
        try:

            logging.info("Entered the start_data_validation method of TrainPipeline class")
            logging.info("Starting Data Validation")
            data_validation = DataValidation(data_validation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifacts)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise objException(e, sys)

    def initate_model_trainer(self,data_validation_artifacts:DataValidationArtifact):
        try:
            logging.info("Entered the initate_model_trainer method of TrainPipeline class")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifact = model_trainer.initate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise objException(e,sys)

    def initate_model_pusher(self,model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info("Entered the initate_model_pusher method of TrainPipeline class")
            model_pusher = ModelPusher(model_pusher_config=self.model_pusher_config,model_trainer_artifact=model_trainer_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise objException(e,sys)
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(
                data_ingestion_artifacts=data_ingestion_artifact,
            )
            
            # Only proceed with model training if validation is successful
            # if data_validation_artifacts.validation_status:
            logging.info("Data validation successful, proceeding with model training")
            model_trainer_artifact = self.initate_model_trainer(data_validation_artifacts=data_validation_artifacts)
            # else:
            #     logging.warning("Data validation failed, skipping model training")
                
            # Only proceed with model pusher if model training is successful
            if model_trainer_artifact:
                logging.info("Model training successful, proceeding with model pusher")
                model_pusher_artifact = self.initate_model_pusher(model_trainer_artifact=model_trainer_artifact)
            else:
                logging.warning("Model training failed, skipping model pusher")
        except Exception as e:
            raise objException(e,sys)
        