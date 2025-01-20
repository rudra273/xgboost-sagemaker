import os
import pandas as pd
from utils.helper import test_function , get_data, upload_data, load_config

test_function() 


def preproces(df):
    # write preprosses setps 
    return df


if __name__ == "__main__":

    config = load_config()
    # Use the input_s3 configuration
    input_s3_config = config.get("s3", {})
    input_file = input_s3_config.get("input_filename")
    df = get_data(input_file)
    df = preproces(df)
    upload_data(df, 'preprossed_file.csv')



