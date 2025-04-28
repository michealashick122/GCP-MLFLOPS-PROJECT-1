import os
import pandas as pd

def check_file_access():
    from config.paths_config import PROCESSED_TRAIN_PATH, PROCESSED_TEST_PATH
    
    print(f"Checking access to training data: {PROCESSED_TRAIN_PATH}")
    print(f"Absolute path: {os.path.abspath(PROCESSED_TRAIN_PATH)}")
    print(f"File exists: {os.path.exists(PROCESSED_TRAIN_PATH)}")
    
    if os.path.exists(PROCESSED_TRAIN_PATH):
        print(f"Is readable: {os.access(PROCESSED_TRAIN_PATH, os.R_OK)}")
        
        # Try to open the file
        try:
            with open(PROCESSED_TRAIN_PATH, 'r') as f:
                print("Successfully opened file for reading")
        except Exception as e:
            print(f"Error opening file: {str(e)}")
    

    print(f"\nChecking access to test data: {PROCESSED_TEST_PATH}")
    print(f"Absolute path: {os.path.abspath(PROCESSED_TEST_PATH)}")
    print(f"File exists: {os.path.exists(PROCESSED_TEST_PATH)}")
    
    if os.path.exists(PROCESSED_TEST_PATH):
        print(f"Is readable: {os.access(PROCESSED_TEST_PATH, os.R_OK)}")

if __name__ == "__main__":
    check_file_access()