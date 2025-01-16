# helper function for module
import os
import pandas as pd

def test_function():
    print("test function called from utils") 
    return None


def get_data(file_name):

    input_path = "/opt/ml/processing/input"

    # Find the input file (assuming there's only one)
    input_files = os.listdir(input_path)
    if not input_files:
        raise ValueError("No input files found in the input directory")
    
    input_file_path = os.path.join(input_path, file_name) 

    print(f"Loading data from: {input_file_path}")

    df = pd.read_csv(input_file_path)    

    print('get data function executed', df.columns)

    return df
 

def upload_data(data, file_name):

    output_path = "/opt/ml/processing/output"
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, file_name) 

    print(f"Saving processed data to: {output_file_path}")

    print('data in upload data funtion', data.columns) 
    data.to_csv(output_file_path, index=False)

    return output_file_path


def get_processed_data():
    
    processed_file_path = "/opt/ml/processing/input/train"
    input_files = [
        os.path.join(processed_file_path, file) 
        for file in os.listdir(processed_file_path) 
        if os.path.isfile(os.path.join(processed_file_path, file))
    ]

    if not input_files:
        raise ValueError('No input files found in the training directory')

    raw_data = [pd.read_csv(file, engine="python") for file in input_files]
    processed_data = pd.concat(raw_data) 

    return processed_data 
