import json
import time
import boto3
import os
from dotenv import load_dotenv

from app.db import SessionLocal
from app.models import Job, JobStatus
from worker.processor import process_job

load_dotenv()

# -----------------------
# AWS SQS Setup
# -----------------------
sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

QUEUE_URL = os.getenv("SQS_QUEUE_URL")


# -----------------------
# Poller
# -----------------------
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
            try:
                body = json.loads(msg["Body"])
                handle_job(body)

                # delete only after successful processing
                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )

            except Exception as e:
                print(f"❌ Failed to process message: {e}")


# -----------------------
# Job Processor
# -----------------------
def handle_job(payload):
    db = SessionLocal()
    job = None

    try:
        job_id = payload.get("job_id")

        if not job_id:
            print("❌ Missing job_id in payload")
            return

        job = db.query(Job).filter(Job.job_id == job_id).first()

        if not job:
            print(f"❌ Job not found in DB: {job_id}")
            return

        # Mark as processing
        job.status = JobStatus.PROCESSING
        db.commit()

        print(f"⚙️ Processing job: {job_id}")

        # Actual job logic
        result = process_job(payload)

        job.status = JobStatus.COMPLETED
        job.result = json.dumps(result)
        db.commit()

        print(f"✅ Job completed: {job_id}")

    except Exception as e:
        print(f"❌ Job failed: {e}")

        if job:
            job.status = JobStatus.FAILED
            db.commit()

    finally:
        db.close()


# -----------------------
# Entry Point
# -----------------------
if __name__ == "__main__":
    poll_sqs()
