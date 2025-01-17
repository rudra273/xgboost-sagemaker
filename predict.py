import logging
import numpy as np
import json
from sagemaker import get_execution_role
from sagemaker.predictor import Predictor
from sagemaker.session import Session
from sagemaker.base_serializers import NumpySerializer 

# Set logging level to debug to capture detailed logs
logging.basicConfig(level=logging.DEBUG)
endpoint = 'sagemaker-xgboost-2025-01-17-12-26-44-338'

# Example: Using an existing endpoint and setting up a predictor
predictor = Predictor(endpoint_name=endpoint, sagemaker_session=Session())

# Your data (example input data as a NumPy array)
sklearn_input = np.array([8.3252,41.0,6.984126984126984,1.0238095238095235,322.0,2.555555555555556,37.88,-122.23]).reshape(1, -1)


# Convert NumPy array to list (as JSON doesn't support NumPy arrays directly)
sklearn_input_list = sklearn_input.tolist()

# Set the serializer to JSON
predictor.serializer = NumpySerializer()

# Triggering prediction, logging will capture the request details
response = predictor.predict(sklearn_input_list)

print(response)
