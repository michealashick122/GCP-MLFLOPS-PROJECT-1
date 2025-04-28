import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from config.paths_config import MODEL_OUTPUT_PATH
from config.model_params import *
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from scipy.stats import randint, uniform
from utils.common_function import *
import mlflow

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.params_dist = LIGHTGMM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS
        
    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from {self.train_path} and {self.test_path}...")
            train_df = load_data(self.train_path)
            logger.info("Train data loaded successfully.")
            test_df = load_data(self.test_path)
            logger.info("Test data loaded successfully.")
            x_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']
            x_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            logger.info("Data loaded and split into features and target variable.")
            return x_train, y_train, x_test, y_test
        except Exception as e:
            logger.error(f"Error in loading and splitting data: {e}")
            raise CustomException("Error while loading and splitting data", e)
            
    def train_lgbm(self,x_train, y_train):
        try:
            logger.info("Starting LightGBM model training...")
            lgbm_model = lgb.LGBMClassifier(random_state=42) 
            logger.info("Performing Randomized Search for hyperparameter tuning...")
            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                verbose=self.random_search_params['verbose'],
                n_jobs=self.random_search_params['n_jobs'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )
            logger.info("Starting model fitting...")
            random_search.fit(x_train, y_train)
            logger.info("Model fitting completed.")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            logger.info("Best parameters found: %s", random_search.best_params_)
            logger.info("Best score: %f", random_search.best_score_)
            logger.info("Model training completed.")
            return best_lgbm_model
        except Exception as e:
            logger.error("Error in model training: %s", str(e))
            raise CustomException("Error while training the model", e)
    def evaluate_model(self, model, x_test, y_test):
        try:
            logger.info("Starting model evaluation...")
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred)
            
            logger.info("Model evaluation completed.")
            logger.info("Accuracy: %f", accuracy)
            logger.info("F1 Score: %f", f1)
            logger.info("Precision: %f", precision)
            logger.info("Recall: %f", recall)
            logger.info("ROC AUC Score: %f", roc_auc)
            
            return {
                'accuracy': accuracy,
                'f1_score': f1,
                'precision': precision,
                'recall': recall,
                'roc_auc': roc_auc
            }
        except Exception as e:
            logger.error("Error in model evaluation: %s", str(e))
            raise CustomException("Error while evaluating the model", e)
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving the trained model...")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}.")
        except Exception as e:
            logger.error("Error in saving the model: %s", str(e))
            raise CustomException("Error while saving the model", e)
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting MLFlow Experiment...")
            logger.info("Starting model training process...")
            logger.info("Loading the dataset to MLFLOW")
            mlflow.log_artifact(self.train_path, artifact_path="artifacts") #Inside MLFlow Datasets folder will be created and train and test data will be saved inside it
            mlflow.log_artifact(self.test_path, artifact_path="artifacts")
            x_train, y_train, x_test, y_test = self.load_and_split_data()
            # Remove this duplicate line:
            # x_train, y_train, x_test, y_test = self.load_and_split_data()
            best_lgbm_model = self.train_lgbm(x_train, y_train)
            self.evaluate_model(best_lgbm_model, x_test, y_test)
            self.save_model(best_lgbm_model)
            mlflow.log_artifact(self.model_output_path) #Logging the best model to MLFlow
            logger.info("Logging the Model to MLFlow is completed")
            mlflow.log_params(best_lgbm_model.get_params()) #Logging the model parameters to MLFlow
            logger.info("Logging model metrics to MLFlow...")
            mlflow.log_metrics(self.evaluate_model(best_lgbm_model, x_test, y_test))
            logger.info("Model metrics logged to MLFlow.")
            logger.info("Model training process completed.")
        except Exception as e:
            logger.error("Error in model training process: %s", str(e))
            raise CustomException("Error while running the model training process", e)
if __name__ == "__main__":
    model_training = ModelTraining(PROCESSED_TRAIN_PATH, PROCESSED_TEST_PATH, MODEL_OUTPUT_PATH)
    model_training.run()
    print(f"MODEL_OUTPUT_PATH: {MODEL_OUTPUT_PATH}")    
        
            
            

