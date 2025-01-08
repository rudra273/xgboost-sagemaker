import os
import pandas as pd
from utils.helper import test_function  

test_function() 

def load_data(data_path):
    """
    Load the dataset
    
    Args:
        data_path (str): Path to the preprocessed data file
    
    Returns:
        pandas.DataFrame: preprocessed dataset
    """

    # Read the preprocessed dataset
    df = pd.read_csv(data_path)    

    # Drop rows with missing values
    df = df.dropna()

    return df
 

# Main execution block
if __name__ == "__main__":

    # Input and output paths from SageMaker Processing
    input_path = "/opt/ml/processing/input"
    output_path = "/opt/ml/processing/output"
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Find the input file (assuming there's only one)
    input_files = os.listdir(input_path)
    if not input_files:
        raise ValueError("No input files found in the input directory")
    
    input_file_path = os.path.join(input_path, 'diabetes.csv') 
    output_file_path = os.path.join(output_path, "processed_diabetes.csv") 
    
    # Execute loading step
    print(f"Loading data from: {input_file_path}")
    processed_data = load_data(input_file_path)
    
    print(f"Saving processed data to: {output_file_path}")
    processed_data.to_csv(output_file_path, index=False, header=False)
    
    print("Processing complete!") 