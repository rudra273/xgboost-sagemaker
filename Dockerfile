FROM 750573229682.dkr.ecr.us-east-1.amazonaws.com/xgboost-sagemaker:latest

# Install required packages
COPY requirements.txt /opt/program/requirements.txt
RUN pip install -r /opt/program/requirements.txt

COPY decision_trees /opt/program/

RUN chmod 755 /opt/program/serve

# Link the program to where SageMaker expects it
RUN ln -s /opt/program/serve /usr/local/bin/serve

# Set up the container environment
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Create required directories
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/input/data

# Set working directory
WORKDIR /opt/program