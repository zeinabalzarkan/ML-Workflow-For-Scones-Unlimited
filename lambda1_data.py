# lambda.py

# -----------------------------
# 1. Data Generation Lambda
# -----------------------------
import json

def data_generation_lambda(event, context):
    """
    Generates the input data for the workflow.
    """
    # Example: here we just return a test S3 image and empty inferences
    body = {
        "s3_bucket": "sagemaker-us-east-1-897729128398",
        "s3_key": "test/bicycle_s_000513.png",
        "image_data": event.get("image_data", ""),  # optional: if testing with base64 image
        "inferences": []
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }

