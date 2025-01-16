import argparse
import os
import joblib
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from utils.helper import get_processed_data, test_function

# def main():
#     # Parse arguments
#     parser = argparse.ArgumentParser()

#     parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR', '/opt/ml/output'))
#     parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR', '/opt/ml/processing/output')) 
#     parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN', '/opt/ml/processing/input/train')) 
    
#     args = parser.parse_args()

#     output_data_dir = '/opt/ml/processing/output'
#     model_dir = '/opt/ml/processing/output'
#     train = '/opt/ml/processing/input/train'
    
#     # Read input files 
#     input_files = [
#         os.path.join(args.train, file) 
#         for file in os.listdir(args.train) 
#         if os.path.isfile(os.path.join(args.train, file))
#     ]

#     print(f"Input files: {input_files}") 
    
#     if not input_files:
#         raise ValueError('No input files found in the training directory')
    
#     # Read and concatenate data
#     raw_data = [pd.read_csv(file, header=None, engine="python") for file in input_files]
#     train_data = pd.concat(raw_data)


#     print(f"Training data shape: {train_data.shape}")
    
#     # Set MLflow tracking URI (if needed)
#     tracking_uri = os.environ.get('MLFLOW_TRACKING_URI')

#     if tracking_uri is None:
#         print('uri not found in environment')
#         tracking_uri = 'arn:aws:sagemaker:us-east-1:750573229682:mlflow-tracking-server/mlflow-tracking-server-sagemaker-poc'

#     print(tracking_uri) 

#     mlflow.set_tracking_uri(tracking_uri) 

#     # Set experiment name
#     experiment_name = 'xgboost-experiment'
#     mlflow.set_experiment(experiment_name)

    
#     # Enable MLflow autologging
#     mlflow.autolog()

#     print("Autologging enabled") 

#     X = train_data.drop(columns=['target'])
#     y = train_data['target']

#     # Convert data to DMatrix format
#     dtrain = xgb.DMatrix(X, label=y)

#     # Set XGBoost parameters
#     params = {
#         'objective': 'reg:squarederror',
#         'max_depth': 4,
#         'eta': 0.1,
#         'eval_metric': 'rmse'
#     }

#     # Train the model
#     model = xgb.train(params, dtrain, num_boost_round=100)

#     joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))

#     run_id = mlflow.last_active_run().info.run_id
#     artifact_path = "model"
#     model_uri = "runs:/{run_id}/{artifact_path}".format(run_id=run_id, artifact_path=artifact_path)
#     model_details = mlflow.register_model(model_uri=model_uri, name="xgboost-experiment-model")


def train():

    data = get_processed_data()

    print(data.head)

    tracking_uri = 'arn:aws:sagemaker:us-east-1:750573229682:mlflow-tracking-server/mlflow-tracking-server-sagemaker-poc'

    X = data.drop(columns=["target"], axis=1)
    y = data["target"]

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

    # Log the model to MLflow
    with mlflow.start_run() as run:

        # Log the trained model
        mlflow.xgboost.log_model(model, "model")

        # Register the model with MLflow
        run_id = mlflow.last_active_run().info.run_id
        artifact_path = "model"
        model_uri = "runs:/{run_id}/{artifact_path}".format(run_id=run_id, artifact_path=artifact_path)
        model_details = mlflow.register_model(model_uri=model_uri, name="xgb-housing-model")

    return None

if __name__ == '__main__':
    train()

