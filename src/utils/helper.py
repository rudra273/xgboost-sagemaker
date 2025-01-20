import os
import yaml
import pandas as pd

def test_function():
    print("test function called from utils") 
    return None

def load_config():
    # Get the path to the config file in the container
    config_path = os.path.join(os.getcwd(), "src/utils/config.yml")  
    with open(config_path, 'r') as file:
        conf = yaml.safe_load(file)
    return conf


def get_data(file_name):
    """
    Load data from a specified file in the input directory.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        pd.DataFrame: The loaded dataset as a DataFrame.

    Raises:
        ValueError: If no input files are found in the input directory.
    """

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
    """
    Save the provided DataFrame to a specified file in the output directory.

    Args:
        data (pd.DataFrame): The dataset to save.
        file_name (str): The name of the file to save the data to.

    Returns:
        str: The full path of the saved file.

    Notes:
        Ensures the output directory exists before saving the file.
    """

    output_path = "/opt/ml/processing/output"
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, file_name) 

    print(f"Saving processed data to: {output_file_path}")

    print('data in upload data funtion', data.columns) 
    data.to_csv(output_file_path, index=False)

    return output_file_path


def get_processed_data():
    """
    Load and concatenate all processed training files from the specified directory.

    Returns:
        pd.DataFrame: A concatenated DataFrame containing all processed training data.

    Raises:
        ValueError: If no input files are found in the training directory.

    Notes:
        Assumes the input files are in CSV format and located in "/opt/ml/processing/input/train".
    """

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
