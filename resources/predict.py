import xgboost as xgb
import numpy as np
import os
import json
import pandas as pd
from flask import Flask, Response, request

app = Flask(__name__)

class XGBoostService:
    @classmethod
    def create_predictor(cls):
        try:
            # Try to get the primary model directory from the environment variable
            model_dir = os.environ["SM_MODEL_DIR"]
        except KeyError:
            # If the environment variable is not set, use the fallback directory
            model_dir = "/opt/ml/model"
        
        # Additional fallback: If the primary path does not exist, use another fallback
        if not os.path.exists(model_dir):
            model_dir = "/opt/ml/processing/input/model"
        print(model_dir)
        model_path = os.path.join(model_dir, 'model.xgb')
        cls.model = xgb.Booster()
        cls.model.load_model(model_path)
        
        return cls.model
        
@app.route("/ping", methods=["GET"])
def health_check():
    """Health check route to verify the model is loaded correctly."""
    status = 200 if XGBoostService.create_predictor() else 404
    return Response(response="\n", status=status, mimetype="application/json")

@app.route("/invocations", methods=["POST"])
def inference():
    """Route to perform inference using the loaded XGBoost model."""
    if not request.is_json:
        return Response(
            response="This predictor only supports JSON data", status=415, mimetype="text/plain"
        )
    
    data = request.get_json()
    # Assuming input data is a list of features
    input_data = np.array(data['inputs']).reshape(1, -1)  # Adjust shape if necessary
    
    try:
        dmatrix = xgb.DMatrix(input_data)
        prediction = XGBoostService.model.predict(dmatrix)
        
        pred_dict = {"predictions": prediction.tolist()}
        
        return Response(response=json.dumps(pred_dict), status=200, mimetype="application/json")
    except Exception as e:
        print(str(e))
        result = {"error": f"Internal server error"}
        return Response(response=result, status=500, mimetype="application/json")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)
