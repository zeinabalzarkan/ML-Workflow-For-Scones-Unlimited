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

