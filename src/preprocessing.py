import os
import pandas as pd
from utils.helper import test_function , get_data, upload_data

test_function() 

# def load_data(data_path):
#     """
#     Load the dataset
    
#     Args:
#         data_path (str): Path to the preprocessed data file
    
#     Returns:
#         pandas.DataFrame: preprocessed dataset
#     """

#     # Read the preprocessed dataset
#     df = pd.read_csv(data_path)    

#     return df


# def preprocess(input_file_name,output_file_name):

#     # Input and output paths from SageMaker Processing
#     input_path = "/opt/ml/processing/input"
#     output_path = "/opt/ml/processing/output"
    
#     # Ensure output directory exists
#     os.makedirs(output_path, exist_ok=True)
    
#     # Find the input file (assuming there's only one)
#     input_files = os.listdir(input_path)
#     if not input_files:
#         raise ValueError("No input files found in the input directory")
    
#     input_file_path = os.path.join(input_path, input_file_name) 
#     output_file_path = os.path.join(output_path, output_file_name) 
    
#     # Execute loading step
#     print(f"Loading data from: {input_file_path}")
#     processed_data = load_data(input_file_path)
    
#     print(f"Saving processed data to: {output_file_path}")
#     processed_data.to_csv(output_file_path, index=False, header=False)
    
#     print("Processing complete!") 

# Main execution block


def preproces(file_name):
   
    df = get_data(file_name)
    # write preprosses setps 

    upload_data(df, 'preprossed_file.csv')

    return None


if __name__ == "__main__":

    preproces('california_housing.csv')

    