import json
import time
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

from app.db import SessionLocal
from app.models import Job, JobStatus
from worker.processor import process_job


sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

QUEUE_URL = os.getenv("SQS_QUEUE_URL")


def poll_sqs():
    print("🚀 Worker started. Listening to SQS...")

    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])
        if not messages:
            continue

        for msg in messages:
            body = json.loads(msg["Body"])
            receipt_handle = msg["ReceiptHandle"]

            handle_job(body)

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=receipt_handle
            )


def handle_job(payload):
    db = SessionLocal()
    job_id = payload["job_id"]

    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        job.status = JobStatus.PROCESSING
        db.commit()

        result = process_job(payload)

        job.status = JobStatus.COMPLETED
        job.result = json.dumps(result)
        db.commit()

        print(f"✅ Job {job_id} completed")

    except Exception as e:
        print(f"❌ Job failed: {e}")
        job.status = JobStatus.FAILED
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    poll_sqs()
