
import os
import sys
import certifi
from pymongo import MongoClient 


from src.entity.artifact_entitiy import DataIngestionArtifact
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()


ca = certifi.where()



MONGO_DB_URI = os.getenv('MONGO_DB_URI')

class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig):
        try :
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_collection_as_dataframe(self): 
        """
        Read data from mongodb and convert to dataframe
        """
        try :
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            
            logging.info('Inititating connection to mongo db')
            self.mongo_client = MongoClient(MONGO_DB_URI,tlsCAFile=ca)
            db = self.mongo_client[database_name]
            collection = db[collection_name]
            logging.info("MongoDB connection establised")
        

            df = pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.to_list():
                df.drop(columns='_id',axis=1, inplace=True)

            df.replace("na",np.nan, inplace=True)
            logging.info("Converted data from collectio to dataframe")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, df:pd.DataFrame):
        """
        Store the dataframe read from mongodb to firestore/raw.csv
        """
        try :
            logging.info("Saving data from mongodb to raw csv file")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_name = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_name, exist_ok=True)
            
            df.to_csv(feature_store_file_path,index=False,header=True)
            # return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self,df):
        """
        This function will perform train test split and also store the train set and test set to data_ingestion\ingested\train.csv and test resp"""
        try :
            test_size = self.data_ingestion_config.train_test_split_ratio            
            train_set, test_set = train_test_split(df, test_size=test_size)
            logging.info("Performed train test split on the dataframe")

            logging.info("Saving train set and test set")
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            dir_name = os.path.dirname(train_file_path)
            os.makedirs(dir_name, exist_ok=True)

            logging.info("Exporting train and test file path.")
            train_set.to_csv(train_file_path,index=False, header=True)
            test_set.to_csv(test_file_path,index=False, header=True)
            logging.info("Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_ingestion(self):
        try :
            df = self.export_collection_as_dataframe()
            self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)

            dataingestionartifact = DataIngestionArtifact(trained_file_path = self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
                   
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)