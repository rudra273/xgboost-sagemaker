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

    return df
 

def upload_data(data, file_name):

    output_path = "/opt/ml/processing/output"
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, file_name) 

    print(f"Saving processed data to: {output_file_path}")
    data.to_csv(output_file_path, index=False, header=0)

    return output_file_path