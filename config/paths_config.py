import os

########## DATA INGESTION ############
RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"

########### DATA PROCESSING ############
PROCESSED_DIR = "artifacts/processed"

# Ensure the processed directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

PROCESSED_TRAIN_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv/train_processed.csv")
PROCESSED_TEST_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv/test_processed.csv")

############# MODEL TRAINING###########
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl" 