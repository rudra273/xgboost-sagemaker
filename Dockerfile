# Use your custom XGBoost SageMaker base image
FROM 750573229682.dkr.ecr.us-east-1.amazonaws.com/xgboost-sagemaker:latest

# Copy your resources (e.g., serve.py, predict.py, nginx.conf, etc.)
COPY resources/*.* /

# Install necessary Python libraries (flask, gunicorn, pandas, etc.)
RUN pip install flask
RUN pip install gunicorn
RUN pip uninstall gevent
RUN pip install gevent
RUN pip install pandas

# Install nginx (if needed for reverse proxy setup)
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for working directory
ENV WORKDIR /

# Set the entry point to run your model service
ENTRYPOINT ["python", "/serve.py"]
