import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()


sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

def send_job_to_queue(payload: dict):
    if not QUEUE_URL:
        raise ValueError("SQS_QUEUE_URL is not set in environment")
    
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
