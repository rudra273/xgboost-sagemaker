import os
import numpy as np
import pandas as pd
import boto3
import mlflow
import sagemaker
from sagemaker import get_execution_role
from sagemaker.serve import SchemaBuilder
from sagemaker.serve import ModelBuilder
from sagemaker.serve.mode.function_pointers import Mode
from mlflow import MlflowClient
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Load the California Housing dataset
data = fetch_california_housing()
X, y = data.data, data.target
feature_names = data.feature_names

# Create a DataFrame for better readability
df = pd.DataFrame(X, columns=feature_names)
df['Target'] = y

df.to_csv('california_housing.csv', index=False) 

# print(df) 

csv = pd.read_csv('california_housing.csv')

print(csv) 



