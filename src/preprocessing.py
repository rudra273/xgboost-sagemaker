"""
Preprocess a dataset and upload the processed data to the specified output location.

Functions:
    - preproces(df): Applies preprocessing steps to the input DataFrame.

Workflow:
    1. Load the configuration file to retrieve input and output file paths.
    2. Fetch the dataset using the input file path.
    3. Apply preprocessing steps to the dataset.
    4. Upload the processed dataset to the specified output file path.
"""

import os
import pandas as pd
from utils.helper import test_function , get_data, upload_data, load_config

test_function() 


def preproces(df):
    """
    Apply preprocessing steps to the input DataFrame.

    Args:
        df (pd.DataFrame): The input dataset to preprocess.

    Returns:
        pd.DataFrame: The preprocessed dataset.
    """

    # write preprosses setps 
    return df


if __name__ == "__main__":

    config = load_config()
    input_s3_config = config.get("s3", {})
    s3 = config.get("s3", {}) 
    input_file = s3.get("input_filename")
    output_file = s3.get("output_filename")


    df = get_data(input_file)

    df = preproces(df)

    upload_data(df, output_file)