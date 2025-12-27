from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db import SessionLocal
from app.models import Job, JobStatus
from app.sqs_client import send_job_to_queue

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs")
def create_job(data: dict, db: Session = Depends(get_db)):
    job_id = str(uuid4())

    job = Job(
        job_id=job_id,
        source_url=data["source_url"],
        source_type=data["type"],
        status=JobStatus.PENDING
    )

    db.add(job)
    db.commit()

    send_job_to_queue({
        "job_id": job_id,
        "source_url": data["source_url"],
        "type": data["type"]
    })

    return {"job_id": job_id, "status": "QUEUED"}


@router.get("/jobs/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        return {"error": "Job not found"}

    return {
        "job_id": job.job_id,
        "status": job.status,
        "result": job.result
    }
