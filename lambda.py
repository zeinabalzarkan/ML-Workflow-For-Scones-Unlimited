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

# -----------------------------
# 2. Image Classification Lambda
# -----------------------------
import boto3
import base64

runtime = boto3.client("sagemaker-runtime")

def image_classification_lambda(event, context):
    """
    Calls the SageMaker endpoint with image data to get predictions.
    """
    try:
        # Ensure body exists
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)  # in case Step Functions sends as string

        # Decode image
        image_data = body.get("image_data")
        if not image_data:
            raise ValueError("No image_data found in the request body")
        image = base64.b64decode(image_data)

        # Call SageMaker endpoint
        response = runtime.invoke_endpoint(
            EndpointName="image-classification-2025-08-30-14-14-43-808",
            ContentType="image/png",
            Body=image
        )

        # Read inference result
        result = response["Body"].read().decode('utf-8')

        # Convert to list if needed
        try:
            inferences = json.loads(result)
        except json.JSONDecodeError:
            inferences = [result]

        body["inferences"] = inferences

        return {
            "statusCode": 200,
            "body": json.dumps(body)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# -----------------------------
# 3. Filter Inferences Lambda
# -----------------------------
THRESHOLD = 0.93

def filter_inferences_lambda(event, context):
    """
    Filters out predictions below the confidence threshold.
    """
    try:
        # Ensure body exists
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        # Get inferences (already a list)
        inferences = body.get("inferences", [])
        if not inferences:
            raise ValueError("No inferences found in the request body")

        # Check threshold
        meets_threshold = any(float(conf) >= THRESHOLD for conf in inferences)

        if meets_threshold:
            return {
                "statusCode": 200,
                "body": json.dumps(body)
            }
        else:
            raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
