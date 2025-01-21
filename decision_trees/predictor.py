# predictor.py
import os
import json
import flask
import xgboost as xgb
import numpy as np

class ScoringService(object):
    model = None
    
    @classmethod
    def get_model(cls):
        if cls.model == None:
            model_path = os.path.join(os.environ['MODEL_PATH'], 'xgboost-model')
            cls.model = xgb.Booster()
            cls.model.load_model(model_path)
        return cls.model
    
    @classmethod
    def predict(cls, input):
        model = cls.get_model()
        dmatrix = xgb.DMatrix(input)
        return model.predict(dmatrix)

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    # Check if the model can be loaded
    try:
        ScoringService.get_model()
        status = 200
    except Exception:
        status = 404
    return flask.Response(response=json.dumps(' '), status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    # Parse input JSON
    data = flask.request.get_json()
    data = np.array(data)
    
    # Predict
    predictions = ScoringService.predict(data)
    
    # Convert to JSON
    results = predictions.tolist()
    
    return flask.Response(response=json.dumps(results), status=200, mimetype='application/json')
