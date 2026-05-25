"""
This is an ETL Task

Create a network data extract class
In this class we have main 2 functions

1. csv_to_json_convertor
Takes filepath for csv data as input
Reads the csv data and convert records to json and return json

2. insert_data_mongodb
Takes the json records, database, collection as parameters
Set records, database, collection
Set mongo_client

"""

import os
import sys

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
from pymongo import MongoClient 
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

class NetworkDataExtract:
    def __init__(self,database, collection):
        logging.info("NetworkDataExtract Constructor")
        try:
            self.database = database
            self.collection = collection
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self, filepath):
        try:
            df = pd.read_csv(filepath)
            records = df.to_dict(orient="records")
            logging.info("Records converted from csv to json")

            return records

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_mongodb(self, records):
        try:
            self.records = records

            logging.info("Initialise MongoClient")
            self.mongo_client = MongoClient(MONGO_DB_URI, tlsCAFile=ca)

            db = self.mongo_client[self.database]
            collection = db[self.collection]

            logging.info("Inserting records to mongodb")
            collection.insert_many(self.records)

            logging.info(f"{len(self.records)} records inserted successfully")
            return(len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":

    FILE_PATH = "Network_Data/phishingData.csv"
    DATABASE = "NetworkSecurity"
    COLLECTION = "phishing_data"

    network_obj = NetworkDataExtract(
        database = DATABASE,
        collection = COLLECTION
    )

    records = network_obj.csv_to_json_convertor(FILE_PATH)

    no_of_records = network_obj.insert_data_mongodb(records)

    print(f"{no_of_records} records inserted successfully")