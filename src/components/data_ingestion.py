import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from dataclasses import dataclass
from pymongo import MongoClient



## intialize the data ingestion configuration

@dataclass
class DataIngestionconfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')


## create a data ingestion class
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion method starts')

        try:
           
            # df=pd.read_csv(os.path.join('notebooks/data','breast_cancer_data.csv'))
            df=self.DataFromMongoDB()

            logging.info('Dataset read as pandas Dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False)

            logging.info("Train test split")
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )



        except Exception as e:
            logging.info('Error occured in Data Ingestion config')

    def DataFromMongoDB(self):         
            uri = "mongodb+srv://priya:mongo-priya@cluster0.6yz2ugn.mongodb.net/?retryWrites=true&w=majority"
            # Connect to MongoDB
            client = MongoClient(uri)
            database = client['MLProject']
            collection = database["breast_cancer_data"]
            # Retrieve all data from the MongoDB collection
            cursor = collection.find()
            # Convert cursor data to a list of dictionaries
            data_list = list(cursor)
            # Create a Pandas DataFrame
            df = pd.DataFrame(data_list)
            return df
