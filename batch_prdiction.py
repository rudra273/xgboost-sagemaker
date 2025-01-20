import logging
import numpy as np

import json
from sagemaker import get_execution_role
from sagemaker.predictor import Predictor
from sagemaker.session import Session
from sagemaker.base_serializers import NumpySerializer 
import mlflow
import boto3
import pandas as pd
from io import StringIO



s3_client = boto3.client('s3')

def get_csv_from_s3(bucket_name, file_key):
    
    try:
        # Fetch the file from S3
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the content of the CSV file
        csv_data = csv_obj['Body'].read().decode('utf-8')
        
        # Use StringIO to read the CSV data into pandas
        data = StringIO(csv_data)
        
        # Load the CSV data into a pandas DataFrame
        df = pd.read_csv(data)
        
        return df
    except Exception as e:
        print(f"Error fetching CSV from S3: {e}")
        return None
    

def save_df_to_s3(df, bucket_name, s3_file_path):

    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Create a buffer to hold the CSV content in memory
    csv_buffer = StringIO()

    # Write DataFrame to the buffer as CSV
    df.to_csv(csv_buffer, index=False)

    # Move the pointer to the beginning of the buffer before uploading to S3
    csv_buffer.seek(0)

    # Upload the CSV to the specified S3 path
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_file_path,
        Body=csv_buffer.getvalue()
    )

    print(f"CSV successfully uploaded to {bucket_name}/{s3_file_path}")


 
    
df = get_csv_from_s3("mlflow-sagemaker-us-east-1-750573229682", "xgb_housing/inout_csv/california_housing.csv")

df = df.drop('Target', axis=1)
print(df.head())

# Set logging level to debug to capture detailed logs
logging.basicConfig(level=logging.DEBUG)
# endpoint = 'sagemaker-xgboost-2025-01-17-12-26-44-338'


# Example: Using an existing endpoint and setting up a predictor
# predictor = Predictor(endpoint_name=endpoint, sagemaker_session=Session())

# Your data (example input data as a NumPy array)
batch_input = df 


model_path = 's3://sagemaker-studio-750573229682-fffkyjouino/models/166/da218539d347432689512c8e496d4f9d/artifacts/model'

loaded_model = mlflow.xgboost.load_model(model_path)

pridiction = loaded_model.predict(batch_input[:5])
pridiction = pd.DataFrame(pridiction)

pridiction.to_csv('pridiction.csv', index=False)

print(pridiction)
save_df_to_s3(pridiction, "mlflow-sagemaker-us-east-1-750573229682" ,"xgb_housing/batch_output")
