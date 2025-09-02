# ML Workflow for Scones Unlimited

This repository demonstrates a **serverless image classification pipeline** for *Scones Unlimited*, built using AWS Lambda, Amazon SageMaker, and AWS Step Functions. The workflow is modular, reproducible, and designed for ease of deployment and monitoring.

---

## 🚀 Project Overview

A complete pipeline to:

1. **Serialize Image Data** from S3 into base64.
2. **Classify the Image** using a deployed SageMaker endpoint.
3. **Filter Inferences** based on a confidence threshold.

These steps are orchestrated via AWS Step Functions to build a seamless serverless workflow.

---

## 📂 Repository Structure

```
.
├── lambda1_data.py           # Lambda to fetch and base64-encode image
├── lambda2_classify.py       # Lambda to invoke SageMaker endpoint
├── lambda3_filter.py         # Lambda to filter low-confidence results
├── step_function.json        # Step Functions state machine definition
├── StepFunctionFlowDiagram.png # Visual workflow diagram
├── output_from_lambda1.json  # Sample output after image serialization
├── output_from_lambda2.json  # Sample output after classification
├── output_from_lambda3.json  # Sample output after filtering
├── starter.ipynb             # Notebook walkthrough and testing
└── README.md                 # This document
```

---

## 🛠️ Deployment Instructions

### Prerequisites:
- AWS account with permissions for Lambda, SageMaker, IAM, S3, and Step Functions.
- A SageMaker inference endpoint.

### Steps:

1. **Deploy the Lambdas**  
   - Create three separate Lambda functions and paste code from `lambda1_data.py`, `lambda2_classify.py`, and `lambda3_filter.py`.

2. **Update `step_function.json`**  
   - Replace the placeholder ARNs with your actual Lambda ARNs in the JSON definition.

3. **Deploy Step Functions**  
   - Go to AWS Step Functions, create a new state machine using `step_function.json`.

4. **Test the Pipeline**  
   - Start the execution with an input similar to:
     ```json
     {
       "s3_bucket": "your-bucket-name",
       "s3_key": "path/to/image.png",
       "image_data": "",
       "inferences": []
     }
     ```
   - Verify the output using the sample JSON files provided.

---

## ✅ Example Outputs

- **After Lambda 1** (`lambda1_data.py`):
  ```json
  {
    "image_data": "<base64 encoded>",
    "s3_bucket": "...",
    "s3_key": "..."
  }
  ```

- **After Lambda 2** (`lambda2_classify.py`):
  ```json
  {
    "inferences": [0.99, 0.01]
  }
  ```

- **After Lambda 3** (`lambda3_filter.py`):
  ```json
  {
    "inferences": [0.99, 0.01],
    "meets_threshold": true
  }
  ```

---

## 📖 References

- [AWS Lambda](https://docs.aws.amazon.com/lambda/)  
- [Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/)  
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/)  

---

## 👩‍💻 Author

Created by **Zeinab AlZarkan** as part of the Udacity AWS Machine Learning Engineer curriculum.
