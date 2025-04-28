import os
import pandas as pd
from google.cloud import storage
# from sklearn import train_test_split
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_function import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config): #this is the constructor ---->NOTE: This config denotes the config.yaml
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name=self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_size"]
        
        
        os.makedirs(RAW_DIR,exist_ok=True) #This will create the directory if it does not exist
        logger.info(f"Data injestion started with {self.bucket_name} and the file is {self.file_name}")
        
    def download_csv_from_gcp(self):
        try:
            client= storage.Client() #This will create a client to access the GCP bucket
            bucket= client.bucket(self.bucket_name) #This will create a bucket object to access the GCP bucket
            blob= bucket.blob(self.file_name) #This will create a blob object to access the file in the GCP bucket (I.e FILE NAME)
            blob.download_to_filename(RAW_FILE_PATH) #This will download the file from the GCP bucket to the local machine
            logger.info(f"CSV file is successfully downloaded from GCP bucket {self.bucket_name} and the file is {self.file_name}")
        except Exception as e:
            logger.error(f"Error while downloading the file from GCP bucket: {e}")
            raise CustomException(f"Filed to download the CSV",e) 
    def split_data(self):
        try:
            logger.info("starting the data splitting process")
            df = pd.read_csv(RAW_FILE_PATH) 
            train_data,test_data = train_test_split(df,train_size= self.train_test_ratio,random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH,index=False) #This will save the train data to the local machine
            test_data.to_csv(TEST_FILE_PATH,index=False) #This will save the test data to the local machine
            logger.info("Data splitting is completed and the files are saved to the local machine")
        except Exception as e:
            logger.error("Error while splitting the data : {e}")
            raise CustomException("Filed to split the data",e)
    def run(self):
        try:
            logger.info("Data ingestion started")
            self.download_csv_from_gcp() #This will download the file from the GCP bucket to the local machine
            self.split_data() #This will split the data into train and test data and save it to the local machine
            logger.info("Data ingestion is completed")
        except Exception as e:
            logger.error(f"Error while running the data ingestion: {e}")
            raise CustomException(f"Filed to run the data ingestion",e)
        finally:
            logger.info("Data ingestion is completed")
if __name__ == "__main__":
    data_ingestion = DataIngestion(config=read_yaml(CONFIG_PATH))
    #data_ingestion.download_csv_from_gcp()
    data_ingestion.run()

            
        