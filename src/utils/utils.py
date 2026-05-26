import os
import sys

import yaml
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging 

import numpy as np
import dill

def read_yaml_file(filepath:str) -> dict:
    try:
        with open(filepath,"r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str ,content:object, replace:bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,"w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(filepath: str, array:np.array):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)

        with open(filepath, 'wb') as file_obj:
            np.save(arr=array, file=file_obj)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def load_numpy_array_data(filepath: str) -> np.array:
    try:
        with open(filepath, 'rb') as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of Utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return dill.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

