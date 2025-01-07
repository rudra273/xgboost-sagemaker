# Import libraries
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# Load dataset
diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert data to DMatrix format (required for XGBoost)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Set XGBoost parameters
params = {
    'objective': 'reg:squarederror',  # Regression task
    'max_depth': 4,
    'eta': 0.1,
    'eval_metric': 'rmse'
}

# Train the model
num_round = 100
model = xgb.train(params, dtrain, num_round)

# Make predictions
preds = model.predict(dtest)

# Evaluate the model
rmse = mean_squared_error(y_test, preds)
print(f"RMSE: {rmse}") 
