import os
import sys

from src.constants import training_pipeline_constants
from src.entity.artifact_entitiy import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

from src.utils.main_utils import read_yaml_file, write_yaml_file

import pandas as pd
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact):

        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(training_pipeline_constants.SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def validate_number_of_columns(self, df:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(df.columns)}") 

            if(len(df.columns) == number_of_columns):
                return True
            return False
                
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def is_numerical_column_exist(self, df: pd.DataFrame)-> bool:
        try:
            numerical_columns = self._schema_config['numerical_columns']

            dataframe_columns = df.columns

            missing_numerical_columns = []

            for column in numerical_columns:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
                return False

            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            drift_detected = False # Consider No drift
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                is_same_dist = ks_2samp(d1, d2)

                if threshold <= is_same_dist.pvalue:
                    drift_found_in_this_column = False
                else:
                    logging.info(f"Drift found in column {column}")
                    drift_found_in_this_column = True
                    drift_detected = True

                report.update({
                    column:{
                        "p_value": float(is_same_dist.pvalue),
                        "drift_status": drift_found_in_this_column
                    }
                })

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            write_yaml_file(file_path = drift_report_file_path, content = report)

            return drift_detected

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def initiate_data_validation(self)-> DataValidationArtifact:

        logging.info("Data Validation initiated")
        try:
            logging.info("Get train test file paths from data ingestion artifacts")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            logging.info("Reading data into dataframes from above files")
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)


            logging.info("Validating numbe of columns")
            train_data_status = self.validate_number_of_columns(train_dataframe)
            test_data_status =self.validate_number_of_columns(test_dataframe)

            if not train_data_status :
                raise Exception("Train dataframe does not contain all columns")
            if not test_data_status:
                raise Exception("Test dataframe does not contain all columns")
            

            logging.info("Validating numerical columns")
            train_numerical_status = self.is_numerical_column_exist(train_dataframe)
            test_numerical_status = self.is_numerical_column_exist(test_dataframe)
            if not train_numerical_status:
                raise Exception("Train dataframe numerical columns missing")
            if not test_numerical_status:
                raise Exception("Test dataframe numerical columns missing")



            logging.info("Detecting dataset drift")            
            drift_detected = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            if drift_detected:
                dir_path = self.data_validation_config.invalid_data_dir
                os.makedirs(dir_path, exist_ok=True)
                train_dataframe.to_csv(
                    self.data_validation_config.invalid_train_file_path,
                    index=False,
                    header=True
                )

                test_dataframe.to_csv(
                    self.data_validation_config.invalid_test_file_path,
                    index=False,
                    header=True
                )
            else:
                dir_path = self.data_validation_config.valid_data_dir
                os.makedirs(dir_path, exist_ok=True)
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,
                    index=False,
                    header=True
                )

                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,
                    index=False,
                    header=True
                )
                


            data_validation_artifact = DataValidationArtifact(
                validation_status = not drift_detected,
                valid_train_file_path = (
                    self.data_validation_config.valid_train_file_path
                    if not drift_detected else None
                ),

                valid_test_file_path = (
                    self.data_validation_config.valid_test_file_path
                    if not drift_detected else None
                ),

                invalid_train_file_path = (
                    self.data_validation_config.invalid_train_file_path
                    if drift_detected else None
                ),

                invalid_test_file_path = (
                    self.data_validation_config.invalid_test_file_path
                    if drift_detected else None
                ),

                drift_report_file_path = (
                    self.data_validation_config.drift_report_file_path
                )
            )

            return data_validation_artifact            


        except Exception as e:
            raise  NetworkSecurityException(e,sys)
        

