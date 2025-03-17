from object.logger import logging
from object.exception import objException
import sys
logging.info(" thsi is inside the mesage")

from object.pipeline.training_pipeline import TrainingPipeline
if __name__=="__main__":
    try:
        training_pipeline= TrainingPipeline()
        training_pipeline.run_pipeline()

    except Exception as e:
        raise objException(e,sys)