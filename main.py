from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.logging.logger import logging
import sys

from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import (
    DataTransformationConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
    DataIngestionConfig
)
from src.exception.exception import NetworkSecurityException

if __name__=='__main__':
    try:
        # Create training pipeline config
        training_pipeline_config = TrainingPipelineConfig()

        # Create data_ingestion config
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        
        # Create data_validation config
        data_validation_config = DataValidationConfig(training_pipeline_config)

        # Create data_transformation config
        data_transformation_config = DataTransformationConfig(training_pipeline_config)

        # logging.info("Testing with test db and collection")
        # data_ingestion_config.database_name = "mydb"
        # data_ingestion_config.collection_name = "test"

        
        logging.info("Data ingestion started")
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data ingestion completed")


        logging.info("Data Validation started")
        data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation completed")   


        logging.info("Data Transformation started")
        data_transformation = DataTransformation(data_transformation_config, data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation completed")   


    except Exception as e:
        raise NetworkSecurityException(e,sys)