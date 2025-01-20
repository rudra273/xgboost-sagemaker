import os
import pandas as pd
from utils.helper import test_function , get_data, upload_data, load_config

test_function() 


def preproces(file_name):
   
    df = get_data(file_name)

    # write preprosses setps 
    upload_data(df, 'preprossed_file.csv')

    return None


if __name__ == "__main__":

    s3 = load_config.get("s3", {}) 
    input_file = s3.get("input_filename") 
    preproces('input_file')


    