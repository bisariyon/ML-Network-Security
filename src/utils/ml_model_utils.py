import sys

from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

class PredictionModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            logging.info("Transforming Given x")
            x_transform = self.preprocessor.transform(x)

            logging.info("Predictions on transformed x")
            y_hat = self.model.predict(x_transform)
            
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)