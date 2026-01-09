import sys 
import os 
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import pandas as pd 
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info('logging started')
        try:
            df=pd.read_csv(os.path.join('notebook/loan_approval.csv'))
            logging.info('data frame read as pandas dataframe')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)
            train_set,test_set=train_test_split(df,test_size=0.30)
            logging.info('initiated train test split')

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('data ingestion completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.info('exception occured at data ingestion')
            raise CustomException(e,sys)
        
if __name__ =='__main__':
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,train_target,test_arr,test_target,_=data_transformation.initiate_data_transformation(train_data_path,test_data_path)