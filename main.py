import yaml
import os
from src.utils.helper import load_config
config = load_config()

# Use the input_s3 configuration
input_s3_config = config.get("input_s3", {})
bucket_name = input_s3_config.get("bucket_name")
region = input_s3_config.get("region")
folder = input_s3_config.get("folder")

print(f"Bucket: {bucket_name}, Region: {region}, Folder: {folder}")
