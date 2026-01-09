import pandas as pd 
import numpy as np 
from src.exception import CustomException 
from src.logger import logging
import sys 
import os
from dataclasses import dataclass
from src.utils import save_object,evaluate_models
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier

@dataclass
class ModelTrainerConfig:
    trained_model_file_path:str=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_training(self,train_features_array,train_target_array,test_features_array,test_target_array):
        try:
            logging.info('spliting Dependent and depenedent')
            X_train,y_train,X_test,y_test=(

                train_features_array,
                train_target_array,
                test_features_array,
                test_target_array
            )

            cat_boost_classifier=CatBoostClassifier()

            model_report=evaluate_models(X_train,y_train,X_test,y_test,{'CatBoostClassifier':cat_boost_classifier})
            logging.info(f'MODEL_REPORT:{model_report}')

            best_model_name='CatBoostClassifier'
            best_model_score=model_report[best_model_name]

            logging.info(f'Best Model Found, Model Name: {best_model_name}, Score: {best_model_score}')

            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=cat_boost_classifier
            )
          
        except Exception as e:
            logging.info('Exception occurred at Model Training')
            raise CustomException(e, sys)




            

        

