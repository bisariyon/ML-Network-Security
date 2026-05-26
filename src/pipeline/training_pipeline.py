from src import pipeline
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

import sys


class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_ingestion(self):
        try:
            logging.info("Data ingestion started")
            data_ingestion_config = DataIngestionConfig(
                self.training_pipeline_config
            )
            data_ingestion = DataIngestion(
                data_ingestion_config
            )
            data_ingestion_artifact = (
                data_ingestion.initiate_data_ingestion()
            )
            logging.info("Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact):
        try:
            logging.info("Data validation started")
            data_validation_config = DataValidationConfig(
                self.training_pipeline_config
            )
            data_validation = DataValidation(
                data_validation_config,
                data_ingestion_artifact
            )
            data_validation_artifact = (
                data_validation.initiate_data_validation()
            )
            logging.info("Data validation completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_transformation(
        self,
        data_validation_artifact
    ):
        try:
            logging.info("Data transformation started")
            data_transformation_config = (
                DataTransformationConfig(
                    self.training_pipeline_config
                )
            )
            data_transformation = DataTransformation(
                data_transformation_config,
                data_validation_artifact
            )
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_trainer(
        self,
        data_transformation_artifact
    ):
        try:
            logging.info("Model trainer started")
            model_trainer_config = ModelTrainerConfig(
                self.training_pipeline_config
            )
            model_trainer = ModelTrainer(
                model_trainer_config,
                data_transformation_artifact
            )
            model_trainer_artifact = (
                model_trainer.initiate_model_trainer()
            )
            logging.info("Model trainer completed")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = (
                self.start_data_ingestion()
            )
            print(data_ingestion_artifact, "\n")
            data_validation_artifact = (
                self.start_data_validation(
                    data_ingestion_artifact
                )
            )
            print(data_validation_artifact, "\n")
            data_transformation_artifact = (
                self.start_data_transformation(
                    data_validation_artifact
                )
            )
            print(data_transformation_artifact, "\n")
            model_trainer_artifact = (
                self.start_model_trainer(
                    data_transformation_artifact
                )
            )
            print(model_trainer_artifact)
            logging.info("Training pipeline completed")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

# if __name__ == "__main__":
#     pipeline = TrainingPipeline()
#     pipeline.run_pipeline()

