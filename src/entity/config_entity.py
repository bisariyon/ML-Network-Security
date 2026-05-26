from calendar import c
from datetime import datetime
import os
from src.constants import training_pipeline_constants

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%d_%m_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline_constants.PIPELINE_NAME
        self.artifact_name=training_pipeline_constants.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp


"""
Artifacts/
└── timestamp/
    └── data_ingestion/
        │
        ├── feature_store/
        │   └── rawPhishingData.csv
        │
        └── ingested/
            ├── train.csv
            └── test.csv
      
"""
class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline_constants.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline_constants.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline_constants.RAW_FILE
        )

        self.training_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline_constants.DATA_INGESTION_INGESTED_DIR,
            training_pipeline_constants.TRAIN_FILE_NAME
        )

        self.testing_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline_constants.DATA_INGESTION_INGESTED_DIR,
            training_pipeline_constants.TEST_FILE_NAME
        )

        self.train_test_split_ratio :float = training_pipeline_constants.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name :str = training_pipeline_constants.DATA_INGESTION_COLLECTION_NAME
        self.database_name :str = training_pipeline_constants.DATA_INGESTION_DATABASE_NAME
"""
Artifacts/
└── timestamp/
    └── data_validation/
        │
        ├── validated/
        │   ├── train.csv
        │   └── test.csv
        │
        ├── invalid/
        │   ├── train.csv
        │   └── test.csv
        │
        └── drift_report/
            └── report.yaml
"""
class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline_constants.DATA_VALIDATION_DIR_NAME,            
        )
        
        self.valid_data_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline_constants.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir = os.path.join(
            self.data_validation_dir,
            training_pipeline_constants.DATA_VALIDATION_INVALID_DIR
        )
        
        self.valid_train_file_path = os.path.join(
            self.valid_data_dir,
            training_pipeline_constants.TRAIN_FILE_NAME
        )
        self.valid_test_file_path = os.path.join(
            self.valid_data_dir,
            training_pipeline_constants.TEST_FILE_NAME
        )
        
        self.invalid_train_file_path = os.path.join(
            self.invalid_data_dir,
            training_pipeline_constants.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path = os.path.join(
            self.invalid_data_dir,
            training_pipeline_constants.TEST_FILE_NAME
        )
        
        self.drift_report_file_path = os.path.join(
            self.data_validation_dir,
            training_pipeline_constants.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline_constants.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )


"""
Artifacts/
└── timestamp/
    └── data_transformation/
        │
        ├── transformed/
        │   ├── train.npy
        │   └── test.npy
        │
        └── transformed_obj/
            └── preprocessing.pkl
"""
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        
        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline_constants.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path = os.path.join(
            self.data_transformation_dir,
            training_pipeline_constants.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline_constants.DATA_TRANSFORMATION_TRAIN_FILE_PATH            
        )
        self.transformed_test_file_path = os.path.join(
            self.data_transformation_dir,
            training_pipeline_constants.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline_constants.DATA_TRANSFORMATION_TEST_FILE_PATH           
        )
        self.transformed_object_file_path = os.path.join(
            self.data_transformation_dir,
            training_pipeline_constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline_constants.DATA_TRANSFORMATION_PREPROCESSING_OBJECT_FILE_NAME
        )

"""
Artifacts/
└── timestamp/
    └── model_trainer/
        └──  trained_model/
            └── model.pkl
"""
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        
        self.model_trainer_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline_constants.MODEL_TRAINER_DIR_NAME
        )

        self.trained_model_dir = os.path.join(
            self.model_trainer_dir,
            training_pipeline_constants.MODEL_TRAINER_TRAINED_MODEL_DIR
        )

        self.trained_model_file_path = os.path.join(
            self.trained_model_dir,
            training_pipeline_constants.MODEL_TRAINER_TRAINED_MODEL_FILE_PATH,
        )
        
        self.expected_accuracy = training_pipeline_constants.MODEL_TRAINER_EXPECTED_ACCURACY_SCORE
        self.overfitting_underfitting_threshold = training_pipeline_constants.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
        


