import sys

from src.constants import training_pipeline_constants
from src.entity.artifact_entitiy import DataTransformationArtifact, DataValidationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

import pandas as pd
import numpy as np

from src.utils.main_utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, 
                 data_transformation_config :DataTransformationConfig, 
                 data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            logging.info("Trying to read from CSV")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(self):
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline_comnstants.py file
        and returns a Pipeline object with the KNNImputer object as the first step.
        """
        logging.info("Entered get_data_trnasformer_object method of Transformation class")

        try:
            imputer = KNNImputer(**training_pipeline_constants.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNImputer with {training_pipeline_constants.DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            preprocessor  = Pipeline(
                steps = [
                    ("imputer",imputer)
                ]
            )
            return preprocessor
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Data Transformation initiated")
        try:
            logging.info("Starting data transformation")

            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Read train and test data sets")

            TARGET_COLUMN = training_pipeline_constants.TARGET_COLUMN

            X_train_df = train_df.drop(columns=TARGET_COLUMN, axis=1)
            y_train_df = train_df[TARGET_COLUMN]
            y_train_df = y_train_df.replace(-1,0)

            # y_train_df.to_csv(
            #     r"D:\MLearning\ML Projects\Project 2 Network security\zz.csv",
            #     index=False
            # )            
            logging.info("Created X_train and y_train")
            
            X_test_df = test_df.drop(columns=TARGET_COLUMN, axis=1)
            y_test_df = test_df[TARGET_COLUMN]
            y_test_df = y_test_df.replace(-1,0)
            logging.info("Created X_test and y_test")

            preprocessor = self.get_data_transformer_object()

            logging.info("Applying preprocessor")
            X_train_arr = preprocessor.fit_transform(X_train_df)
            X_test_arr = preprocessor.transform(X_test_df)
            logging.info("Preprocessing completed")

            train_arr = np.column_stack(
                (
                    X_train_arr,
                    np.array(y_train_df)
                )
            )            
            logging.info("Combined X_train y_train to form training dataset")

            test_arr = np.c_[
                X_test_arr,
                np.array(y_test_df)
            ]
            logging.info("Combined X_test y_test to form testing dataset")

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            logging.info("Numpy arrays saved")

            save_object(
                file_path = self.data_transformation_config.transformed_object_file_path,
                obj =  preprocessor
            )
            logging.info("Saved preprocessing object")

            # logging.info("For simplifity saving preprocessor object to final_model/preprocessor.pkl")
            # save_object( "final_model/preprocessor.pkl", preprocessor)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)


        