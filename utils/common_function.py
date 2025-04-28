import os
import yaml
from src.logger import get_logger
from src.custom_exception import CustomException
import pandas as pd

logger = get_logger(__name__)


def read_yaml(filepath):
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError("File is not found in the given path.")
        with open(filepath, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config
    except Exception as e:
        logger.error("Error while reading logger file.", e)
        raise CustomException("Failed to read YAML file", e)
        
# def load_data(file_path):
#     try:
#         # Check if the directory exists
#         directory = os.path.dirname(file_path)
#         if not os.path.exists(directory):
#             os.makedirs(directory, exist_ok=True)
#             logger.info(f"Created directory: {directory}")
            
#         logger.info(f"Reading CSV file: {file_path}")
#         data = pd.read_csv(file_path)
#         logger.info(f"Data loaded successfully from {file_path}")
#         return data
#     except PermissionError as e:
#         logger.error(f"Permission denied while accessing {file_path}: {str(e)}")
#         raise CustomException(f"Permission denied for file: {file_path}", e)
#     except Exception as e:
#         logger.error(f"Error loading data from {file_path}: {str(e)}")
#         raise CustomException(f"Failed to load data from {file_path}", e)

def load_data(file_path):
    try:
        # Log the file being accessed
        logger.info(f"Reading CSV file: {file_path}")
        
        # Ensure file exists before attempting to read
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}")
        return data

    except PermissionError as e:
        logger.error(f"Permission denied while accessing {file_path}: {str(e)}")
        raise CustomException(f"Permission denied for file: {file_path}", e)
    except FileNotFoundError as e:
        logger.error(str(e))
        raise CustomException(str(e), e)
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {str(e)}")
        raise CustomException(f"Failed to load data from {file_path}", e)