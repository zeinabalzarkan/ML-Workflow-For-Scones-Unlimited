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
