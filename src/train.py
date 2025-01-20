import argparse
import os
import joblib
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from utils.helper import get_processed_data, test_function, load_config

test_function()

def train(data, mlflow_uri=None, experiment_name='default', model_name="example"):
    """
    Train a machine learning model using the provided dataset and log the model to MLflow.

    Args:
        data (pd.DataFrame): The preprocessed dataset containing features and the target variable.
                             The target column must be named 'Target'.
        mlflow_uri (str): The URI of the MLflow tracking server.
        experiment_name (str, optional): The name of the MLflow experiment to log the model under. Defaults to 'default'.
        model_name (str, optional): The name of the model to register in mlflow
    Returns:
        None
    """

    model_dir = '/opt/ml/processing/output'

    mlflow.set_tracking_uri(mlflow_uri)

    # Set experiment name
    mlflow.set_experiment(experiment_name)

    # write training code...
    X = data.drop(columns=["Target"], axis=1)
    y = data["Target"]

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the XGBRegressor
    model = XGBRegressor(
        n_estimators=100,        # Number of boosting rounds
        learning_rate=0.1,       # Learning rate
        max_depth=6,             # Maximum depth of trees
        subsample=0.8,           # Fraction of samples used per tree
        colsample_bytree=0.8,    # Fraction of features used per tree
        random_state=42          # For reproducibility
    )

    # Train the model
    model.fit(
        X_train, y_train,
    )

    joblib.dump(model, os.path.join(model_dir, "model.joblib"))

    # Log the model to MLflow
    with mlflow.start_run() as run:

        # Log the trained model
        mlflow.xgboost.log_model(model, "model")

        # Register the model with MLflow
        run_id = mlflow.last_active_run().info.run_id
        artifact_path = "model"
        model_uri = "runs:/{run_id}/{artifact_path}".format(run_id=run_id, artifact_path=artifact_path)
        model_details = mlflow.register_model(model_uri=model_uri, name=model_name)

    return None

if __name__ == '__main__':

    config = load_config()
    sagemaker = config.get("sagemaker", {}) 

    data = get_processed_data()

    # mlflow_tracking_uri = 'arn:aws:sagemaker:us-east-1:750573229682:mlflow-tracking-server/mlflow-tracking-server-sagemaker-poc'
    # experiment_name = 'xgboost-housing-regression'
    # model_name = "xgb-housing-model"

    mlflow_tracking_uri = sagemaker.get("mlflow_tracking_uri")
    experiment_name = sagemaker.get("experiment_name"),
    model_name = sagemaker.get("model_name")

    train(data, mlflow_tracking_uri, experiment_name, model_name)

