import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_function import load_data , read_yaml
from sklearn.preprocessing import StandardScaler , LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__ (self,train_path, test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = config_path
        self.config = read_yaml(config_path)
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Directory {self.processed_dir} created.")
    def preprocess_data(self,df):
        try:
            logger.info("Starting data preprocessing...")
            logger.info("Dropping columns...")
            df.drop(columns=['Booking_ID'],inplace=True)
            df.drop_duplicates(inplace=True)
            
            cat_cols = self.config["data_processing"]["categorical_features"]
            num_cols = self.config["data_processing"]["numerical_features"]
            logger.info("Starting label encoding...")
            le = LabelEncoder()
            for col in cat_cols:
                df[col] = le.fit_transform(df[col])
            logger.info("Label encoding completed.")
            
            logger.info("Skewness handling started...")
            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())
            for column in skewness[skewness> skewness_threshold].index:
                if skewness[column] > 0:
                    df[column] = np.log1p(df[column])
                else:
                    df[column] = np.expm1(df[column])
            logger.info("Skewness handling completed.")
            return df
        except Exception as e:
            logger.error("Error in data preprocessing: %s", str(e))
            raise CustomException("Error while data pre-processing", e)   
    def balance_data(self,df):
         try:
             logger.info("Starting data balancing...")
             x = df.drop(columns=['booking_status'])
             y = df['booking_status']
             smote = SMOTE(random_state=42)
             x_resampled, y_resampled = smote.fit_resample(x,y)
             balanced_df = pd.DataFrame(x_resampled, columns=x.columns)
             balanced_df['booking_status'] = y_resampled
             balanced_df.to_csv('balanced_train.csv', index=False)
             logger.info("Data balancing completed.")
             return balanced_df
         except Exception as e:
                logger.error("Error in data balancing: %s", str(e))
                raise CustomException("Error while data balancing", e)
    def select_features(self,df):
        try:
            logger.info("Starting feature selection...")
            x= df.drop(columns=['booking_status'])
            y = df['booking_status']
            model =RandomForestClassifier()
            model.fit(x, y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': feature_importance})
            top_feature_imp_df = feature_importance_df.sort_values(by='Importance', ascending=False)
            num_features_to_select = self.config["data_processing"]["no_of_features"]
            top_ten_features = top_feature_imp_df['Feature'].head(num_features_to_select).values
            top_ten_df = df[top_ten_features.tolist() + ['booking_status']]
            logger.info("Feature selection completed.")
            return top_ten_df
        except Exception as e:
            logger.error("Error in feature selection: %s", str(e))
            raise CustomException("Error while feature selection", e)
    def save_data(self,df,file_path):
        try:
            logger.info("Saving data...")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved to {file_path}.")
        except Exception as e:
            logger.error("Error in saving data: %s", str(e))
            raise CustomException("Error while saving data", e)
    def process(self):
        try:
            logger.info("Loading data from RAW files...")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            logger.info("Data loaded successfully.")
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)
            train_df = self.select_features(train_df)
            test_df = train_df[train_df.columns]
            os.makedirs(PROCESSED_TRAIN_PATH, exist_ok=True)
            os.makedirs(PROCESSED_TEST_PATH, exist_ok=True)
            self.save_data(train_df, os.path.join(PROCESSED_TRAIN_PATH, 'train_processed.csv'))
            self.save_data(test_df, os.path.join(PROCESSED_TEST_PATH, 'test_processed.csv'))
            logger.info("Data processing completed.")
        except Exception as e:
            logger.error("Error in data processing: %s", str(e))
            raise CustomException("Error while data processing", e)
        
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()
    print(f"PROCESSED_TRAIN_PATH: {PROCESSED_TRAIN_PATH}")
    print(f"Directory exists: {os.path.exists(os.path.dirname(PROCESSED_TRAIN_PATH))}")





