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
    tracking_uri = os.environ.get('MLFLOW_TRACKING_URI')

    print(tracking_uri)

    if tracking_uri is None:
        print('uri not found in environment')
        tracking_uri = 'arn:aws:sagemaker:us-east-1:750573229682:mlflow-tracking-server/mlflow-tracking-server-sagemaker-poc'

    print(tracking_uri)

    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    
    # Get the latest version of the registered model
    registered_model = client.get_registered_model(name=model_name)
    return registered_model.latest_versions[0].source


def main():
    region_name = "us-east-1" 
    boto3.setup_default_session(region_name=region_name)
    sagemaker_session = Session()

    # role = get_execution_role(sagemaker_session=sagemaker_session)

    role = 'arn:aws:iam::750573229682:role/service-role/AmazonSageMaker-ExecutionRole-20241211T150457'
    
    # Get the latest model source from MLflow
    # source_path = get_latest_model_source("xgb-housing-model")

    source_path = 's3://sagemaker-studio-750573229682-fffkyjouino/models/166/7f0ef80fc0e347b18004c360205e73c4/artifacts/model'

    sample_input = np.array([8.3252,41.0,6.984126984126984,1.0238095238095235,322.0,2.555555555555556,37.88,-122.23]).reshape(1, -1)

    sample_output = 4.526
    sklearn_schema_builder = SchemaBuilder(
        sample_input=sample_input,
        sample_output=sample_output,
    )

    # Create model builder with the schema builder.
    model_builder = ModelBuilder(
        mode=Mode.SAGEMAKER_ENDPOINT,
        schema_builder=sklearn_schema_builder,
        role_arn=role,
        model_metadata={"MLFLOW_MODEL_PATH": source_path},
    )

    built_model = model_builder.build()

    predictor = built_model.deploy(initial_instance_count=1, instance_type="ml.m5.large")
    
    # Optional: Test the predictor
    prediction = predictor.predict(sample_input)
    print("Model prediction:", prediction)

if __name__ == '__main__':
    main()

