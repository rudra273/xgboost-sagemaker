import yaml
import os
from src.utils.helper import load_config
config = load_config()

# Use the input_s3 configuration
input_s3_config = config.get("s3", {})
bucket_name = input_s3_config.get("input_bucket_name")


print(f"Bucket: {bucket_name}")
