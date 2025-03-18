import os, sys
import shutil
import urllib.request  # Added missing import
from object.exception import objException
from object.logger import logger, logging
from object.constant import *
from object.entity.artifacts_entity import *
from object.entity.config_entity import *


class ModelTrainer:
    def __init__(self, data_validation_artifacts: DataValidationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_validation_artifact = data_validation_artifacts
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise objException(e, sys)
        
    def initate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info(f"{'>>'*20} Model Training {'<<'*20}")
        try:
            logging.info("unzipping the data")
            import zipfile
            
            # Get the correct path to the zip file from data ingestion artifact
            # The zip file should be in the feature_store_path from data ingestion
            zip_file_path = self.data_validation_artifact.data_ingestion_artifact.data_zip_file_path
            
            logging.info(f"Using zip file path: {zip_file_path}")
            
            if not os.path.exists(zip_file_path):
                logging.error(f"Zip file not found at {zip_file_path}")
                raise Exception(f"Zip file not found at {zip_file_path}")
                
            extract_dir = os.getcwd()
            
            logging.info(f"Extracting {zip_file_path} to {extract_dir}")
            
            # Extract the zip file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Check if the expected directories exist
            train_img_path = os.path.join(os.getcwd(), "images", "train")
            val_img_path = os.path.join(os.getcwd(), "images", "valid")
            
            logging.info(f"Checking if train path exists: {train_img_path}")
            logging.info(f"Checking if validation path exists: {val_img_path}")
            
            # Make sure the directories exist
            if not os.path.exists(train_img_path):
                raise Exception(f"Train image directory not found at {train_img_path}. Check the extracted zip structure.")
            
            if not os.path.exists(val_img_path):
                raise Exception(f"Validation image directory not found at {val_img_path}. Check the extracted zip structure.")

            # Training images
            with open('train.txt', "w+") as f:  # Changed to w+ to overwrite any existing file
                img_list = os.listdir(train_img_path)
                for img in img_list:
                    f.write(os.path.join(train_img_path, img) + '\n')
                logging.info("Done writing Training images paths")

            # Validation Image
            with open('val.txt', "w+") as f:  # Changed to w+ to overwrite any existing file
                img_list = os.listdir(val_img_path)
                for img in img_list:
                    f.write(os.path.join(val_img_path, img) + '\n')
                logging.info("Done writing Validation Image paths")

            url = self.model_trainer_config.model_weights_url
            file_name = os.path.basename(url)
            
            # Create yolov7 directory if it doesn't exist
            os.makedirs("yolov7", exist_ok=True)
            
            # Download the weights
            urllib.request.urlretrieve(url, os.path.join("yolov7", file_name))
            logging.info(f"Downloaded weights from {url}")

            # Training - use subprocess for Windows compatibility
            import subprocess
            
            # Change directory to yolov7 and run the training command
            train_cmd = [
                "python", "train.py",
                "--batch", str(self.model_trainer_config.model_batch_size),
                "--cfg", "cfg/training/custom_yolov7.yaml",
                "--epochs", str(self.model_trainer_config.model_epochs),
                "--data", "data/custom.yaml",
                "--weights", "yolov7.pt"
            ]
            
            logging.info(f"Running training command: {' '.join(train_cmd)}")
            subprocess.run(train_cmd, cwd="yolov7", check=True)

            # Copy the best model
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            
            # Use shutil for file operations instead of system commands
            best_model_path = os.path.join("yolov7", "runs", "train", "exp", "weights", "best.pt")
            if os.path.exists(best_model_path):
                shutil.copy(best_model_path, "yolov7/")
                shutil.copy(best_model_path, self.model_trainer_config.model_trainer_dir)
                logging.info(f"Copied best model to {self.model_trainer_config.model_trainer_dir}")
            else:
                logging.error(f"Best model not found at {best_model_path}")

            # Clean up - use shutil and os for Windows compatibility
            if os.path.exists("yolov7/runs"):
                shutil.rmtree("yolov7/runs")
            
            for item in ["images", "labels"]:
                if os.path.exists(item):
                    shutil.rmtree(item)
            
            for file in ["classes.names", "train.txt", "val.txt", "train.cache", "val.cache"]:
                if os.path.exists(file):
                    os.remove(file)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov7/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            logging.error(f"Error in model training: {str(e)}")
            raise objException(e, sys)