import os
import sys
import dagshub
dagshub.init(repo_owner='bisariyon', repo_name='ML-Network-Security', mlflow=True)

import mlflow
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from src.entity.artifact_entitiy import DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.utils.main_utils import evaluate_model, load_numpy_array_data, load_object, save_object
from src.utils.ml_metric_utils import get_classification_score

from src.utils.ml_model_utils import PredictionModel

class ModelTrainer:
    def __init__(self, 
                 model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model,classification_metric, best_model_name):
        

        with mlflow.start_run():
            f1_score=classification_metric.f1_score
            precision_score=classification_metric.precision_score
            recall_score=classification_metric.recall_score

        
            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)

            mlflow.log_param("best_model", best_model_name)

            mlflow.sklearn.log_model(best_model,"model")



    def train_model(self,X_train,y_train,X_test,y_test):

        models = {
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                # 'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                'loss':['log_loss', 'exponential'],
                # 'learning_rate':[.1,.01,.05,.001],
                # 'subsample':[0.6,0.7,0.75,0.85,0.9],
                'criterion':['squared_error', 'friedman_mse'],
                'max_features':['auto','sqrt','log2'],
                # 'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                # 'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        logging.info("Now sending data for model fititng and evaluation")
        model_report, trained_models = evaluate_model(X_train, y_train, X_test, y_test, models, params)

        best_model_name = max(model_report, key=model_report.get)
        best_model = trained_models[best_model_name]
        logging.info(f"Model trained and best model is {best_model_name} : {best_model}")

        logging.info("Using best model to predict on train data")
        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_true = y_train,y_pred=y_train_pred)

        logging.info("Track mlfow on train data")
        self.track_mlflow(best_model,classification_train_metric,best_model_name)
        

        logging.info("Using best model to predict on test data")
        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_true = y_test,y_pred=y_test_pred)

        logging.info("Track mlfow on test data")
        self.track_mlflow(best_model,classification_test_metric,best_model_name)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        logging.info("Preprocessor loaded")

        logging.info("Creating directory to store trained model")
        trained_model_dir = self.model_trainer_config.trained_model_dir
        os.makedirs(trained_model_dir, exist_ok=True)

        prediction_model  = PredictionModel(preprocessor=preprocessor,model=best_model)
        logging.info("Create prediction_model from existing preprocessor and best model")

        save_object(self.model_trainer_config.trained_model_file_path,obj = prediction_model)
        logging.info("prediction_model saved to artifacts\<date.now()>\model_trainer\trained_model\model.pkl")      

        model_trainer_artifact  = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, 
                                                       train_metric_artifact = classification_train_metric,
                                                       test_metric_artifact=classification_test_metric )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact 

    def initiate_model_trainer(self):
        logging.info("Model trainer initiated")
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            logging.info("Obtained Train and test file paths")

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            logging.info("Load train arr and test array from numpy array")

            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            logging.info(f"Created the X_train, y_train, X_test, y_test")

            model_trainer_artifact=self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

