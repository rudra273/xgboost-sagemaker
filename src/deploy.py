import os
import numpy as np
import sagemaker
from sagemaker.serve import SchemaBuilder, ModelBuilder
from sagemaker.serve.mode.function_pointers import Mode
import mlflow
from mlflow import MlflowClient
import boto3
from sagemaker import get_execution_role, Session

def get_latest_model_source(model_name):
    """
    Retrieve the latest model source from MLflow registry
    
    Args:
        model_name (str): Name of the registered model
    
    Returns:
        str: Source path of the latest model version
    """

    # Set MLflow tracking URI (if needed)
    
    tracking_uri = 'arn:aws:sagemaker:us-east-1:750573229682:mlflow-tracking-server/mlflow-tracking-server-sagemaker-poc'

    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    
    # Get the latest version of the registered model
    registered_model = client.get_registered_model(name=model_name)
    return registered_model.latest_versions[0].source


def sg_schema_builder():
    """
    Build a schema for input and output data using sample values.

    Returns:
        SchemaBuilder: An instance of SchemaBuilder containing the schema
                       for the sample input and output data.

    Notes:
        - The input sample is reshaped into a 2D array suitable for model input.
        - The output sample represents a target value corresponding to the input.
    """

    xgb_housing_input = np.array([8.3252,41.0,6.984126984126984,1.0238095238095235,322.0,2.555555555555556,37.88,-122.23]).reshape(1, -1)
    
    xgb_housing_output = 0.59980532

    sb = SchemaBuilder(
        sample_input=xgb_housing_input,
        sample_output=xgb_housing_output,
    )
    return sb

def deploy_model(source_path, execution_role, schema_builder, instance_type):
    """
    Deploy a machine learning model to SageMaker using the provided schema and configuration.

    Args:
        source_path (str): The path to the model artifact in MLflow.
        execution_role (str): The execution role ARN for SageMaker.
        schema_builder (SchemaBuilder): The schema builder instance containing input and output data schemas.

    Returns:
        predictor: A deployed SageMaker endpoint predictor.

    Notes:
        - The function uses the provided schema builder and execution role to build and deploy a model to SageMaker.
        - The model is deployed with a single instance of type 'ml.m5.large'.
        - Optionally, the predictor can be used to test predictions after deployment.
    """

    # xgb_housing_input = np.array([8.3252,41.0,6.984126984126984,1.0238095238095235,322.0,2.555555555555556,37.88,-122.23]).reshape(1, -1)
    
    # xgb_housing_output = 0.59980532


    # sklearn_schema_builder = SchemaBuilder(
    #     sample_input=xgb_housing_input,
    #     sample_output=xgb_housing_output,
    # )

    # Create model builder with the schema builder.
    model_builder = ModelBuilder(
        mode=Mode.SAGEMAKER_ENDPOINT,
        schema_builder=schema_builder,
        role_arn=execution_role,
        model_metadata={"MLFLOW_MODEL_PATH": source_path},
    )

    built_model = model_builder.build()

    predictor = built_model.deploy(initial_instance_count=1, instance_type=instance_type)
    
    # Optional: Test the predictor
    # prediction = predictor.predict(xgb_housing_input)
    # print("Model prediction:", prediction) 

if __name__ == '__main__':
    region_name = "us-east-1" 
    boto3.setup_default_session(region_name=region_name)
    sagemaker_session = Session()

    # execution_role = get_execution_role(sagemaker_session=sagemaker_session)
    
    # Get the latest model source from MLflow

    model_name = "xgb-housing-model"
    source_path = get_latest_model_source(model_name)
    execution_role = 'arn:aws:iam::750573229682:role/service-role/AmazonSageMaker-ExecutionRole-20241211T150457' 
    schema_builder = sg_schema_builder()
    instance_type = "ml.m5.large"

    deploy_model(source_path, execution_role, schema_builder, instance_type) 

