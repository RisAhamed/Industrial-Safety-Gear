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
            
            # Get the correct path to the data from data ingestion artifact
            feature_store_path = self.data_validation_artifact.data_ingestion_artifact.feature_store_path
            zip_file_path = self.data_validation_artifact.data_ingestion_artifact.data_zip_file_path
            
            logging.info(f"Using feature store path: {feature_store_path}")
            logging.info(f"Using zip file path: {zip_file_path}")
            
            extract_dir = os.getcwd()
            logging.info(f"Extracting to: {extract_dir}")
            # Check if we need to extract from zip or copy from feature store
            if os.path.isfile(zip_file_path) and zip_file_path.endswith('.zip'):
                logging.info(f"Extracting zip file: {zip_file_path} to {extract_dir}")
                
                # Extract the zip file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                logging.info("Zip file extracted successfully")
            else:
                # If not a zip file, copy the data from feature store to current directory
                logging.info(f"Copying data from feature store: {feature_store_path} to current directory")
                
                # Check if feature store path exists and is a directory
                if os.path.isdir(feature_store_path):
                    # Copy all contents from feature store to current directory
                    for item in os.listdir(feature_store_path):
                        source = os.path.join(feature_store_path, item)
                        destination = os.path.join(extract_dir, item)
                        
                        if os.path.isdir(source):
                            if os.path.exists(destination):
                                shutil.rmtree(destination)
                            shutil.copytree(source, destination)
                            logging.info(f"Copied directory: {item}")
                        else:
                            shutil.copy2(source, destination)
                            logging.info(f"Copied file: {item}")
                else:
                    logging.error(f"Feature store path is not a directory: {feature_store_path}")
                    raise Exception(f"Feature store path is not a directory: {feature_store_path}")
            
            # Check if the expected directories exist
            train_img_path = os.path.join(os.getcwd(), "train", "images")
            val_img_path = os.path.join(os.getcwd(), "valid", "images")
            train_label_path = os.path.join(os.getcwd(), "train", "labels")
            
            logging.info(f"Checking if train path exists: {train_img_path}")
            logging.info(f"Checking if validation path exists: {val_img_path}")
            
            # Make sure the directories exist
            if not os.path.exists(train_img_path):
                raise Exception(f"Train image directory not found at {train_img_path}. Check the extracted zip structure.")
            
            if not os.path.exists(val_img_path):
                raise Exception(f"Validation image directory not found at {val_img_path}. Check the extracted zip structure.")

            # Training images
            with open('train.txt', "w+") as f:
                img_list = os.listdir(train_img_path)
                for img in img_list:
                    f.write(os.path.join(train_img_path, img) + '\n')
                logging.info("Done writing Training images paths")

            # Validation Image
            with open('val.txt', "w+") as f:
                img_list = os.listdir(val_img_path)
                for img in img_list:
                    f.write(os.path.join(val_img_path, img) + '\n')
                logging.info("Done writing Validation Image paths")

            # Determine the number of classes by analyzing the label files
            max_class_id = 0
            if os.path.exists(train_label_path):
                for label_file in os.listdir(train_label_path):
                    if label_file.endswith('.txt'):
                        with open(os.path.join(train_label_path, label_file), 'r') as lf:
                            for line in lf:
                                if line.strip():
                                    class_id = int(line.strip().split()[0])
                                    max_class_id = max(max_class_id, class_id)
            
            # Number of classes is max_class_id + 1 (since class IDs start from 0)
            num_classes = max_class_id + 1
            logging.info(f"Detected {num_classes} classes from label files")

            # Create custom.yaml file for YOLOv7
            os.makedirs(os.path.join("yolov7", "data"), exist_ok=True)
            custom_yaml_path = os.path.join("yolov7", "data", "custom.yaml")
            
            # Create a basic custom.yaml file with the necessary configuration
            with open(custom_yaml_path, 'w') as f:
                # Write the YAML configuration
                yaml_content = f"""# YOLOv7 configuration
            train: {os.path.abspath('train.txt')}
            val: {os.path.abspath('val.txt')}
            test: {os.path.abspath('val.txt')}
            
            # number of classes
            nc: {num_classes}
            
            # class names
            names: ["""
                
                # Add class names (using generic names if actual names are unknown)
                for i in range(num_classes):
                    if i > 0:
                        yaml_content += ", "
                    yaml_content += f"'class{i}'"
                
                yaml_content += "]\n"
                f.write(yaml_content)
            
            logging.info(f"Created custom.yaml with {num_classes} classes")

            # Update the custom_yolov7.yaml file to match the number of classes
            cfg_dir = os.path.join("yolov7", "cfg", "training")
            os.makedirs(cfg_dir, exist_ok=True)
            
            custom_cfg_path = os.path.join(cfg_dir, "custom_yolov7.yaml")
            
            # Check if yolov7.yaml exists in the repository
            yolov7_cfg_path = os.path.join("yolov7", "cfg", "training", "yolov7.yaml")
            if os.path.exists(yolov7_cfg_path):
                # Read the yolov7.yaml file
                with open(yolov7_cfg_path, 'r') as f:
                    cfg_content = f.read()
                
                # Replace the number of classes
                cfg_content = cfg_content.replace("nc: 80", f"nc: {num_classes}")
                
                # Write the updated content to custom_yolov7.yaml
                with open(custom_cfg_path, 'w') as f:
                    f.write(cfg_content)
                
                logging.info(f"Created custom_yolov7.yaml with {num_classes} classes")
            else:
                # Create a basic custom_yolov7.yaml file
                with open(custom_cfg_path, 'w') as f:
                    f.write(f"""# Parameters
            nc: {num_classes}  # number of classes
            depth_multiple: 1.0  # model depth multiple
            width_multiple: 1.0  # layer channel multiple
            
            # anchors
            anchors:
              - [12,16, 19,36, 40,28]  # P3/8
              - [36,75, 76,55, 72,146]  # P4/16
              - [142,110, 192,243, 459,401]  # P5/32
            
            # YOLOv7 backbone
            backbone:
              # [from, number, module, args]
              [[-1, 1, Conv, [32, 3, 1]],  # 0
               [-1, 1, Conv, [64, 3, 2]],  # 1-P1/2
               [-1, 1, Conv, [64, 3, 1]],
               [-1, 1, Conv, [128, 3, 2]],  # 3-P2/4
               # ... rest of backbone configuration ...
              ]
            
            # YOLOv7 head
            head:
              [[-1, 1, Conv, [512, 1, 1]],
               # ... rest of head configuration ...
              ]
            """)
                logging.info(f"Created basic custom_yolov7.yaml with {num_classes} classes")

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
                "--batch", str(max(2, self.model_trainer_config.model_batch_size // 4)),  # Adjusted for CPU
                "--cfg", "cfg/training/custom_yolov7.yaml",
                "--epochs", str(min(50, self.model_trainer_config.model_epochs)),         # Reduced for CPU
                "--data", "data/custom.yaml",
                "--weights", "yolov7.pt",
                "--device", "cpu"  # Ensures CPU usage
            ]
            
            logging.info(f"Running training command: {' '.join(train_cmd)}")
            subprocess.run(train_cmd, cwd="yolov7", check=True)

            # Copy the best model
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            
            # Get the latest experiment directory (could be exp, exp1, exp2, etc.)
            runs_dir = os.path.join("yolov7", "runs", "train")
            if os.path.exists(runs_dir):
                exp_dirs = [d for d in os.listdir(runs_dir) if d.startswith("exp")]
                if exp_dirs:
                    # Sort to get the latest experiment directory
                    latest_exp = sorted(exp_dirs)[-1]
                    best_model_path = os.path.join(runs_dir, latest_exp, "weights", "best.pt")
                    
                    logging.info(f"Looking for best model at: {best_model_path}")
                    
                    if os.path.exists(best_model_path):
                        # Copy the model to yolov7 directory and model_trainer_dir
                        shutil.copy(best_model_path, "yolov7/")
                        shutil.copy(best_model_path, self.model_trainer_config.model_trainer_dir)
                        logging.info(f"Copied best model to {self.model_trainer_config.model_trainer_dir}")
                    else:
                        logging.error(f"Best model not found at {best_model_path}")
                else:
                    logging.error("No experiment directories found in runs/train")
            else:
                logging.error(f"Runs directory not found at {runs_dir}")

            # Clean up - use shutil and os for Windows compatibility
            # IMPORTANT: Only clean up AFTER copying the model files
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