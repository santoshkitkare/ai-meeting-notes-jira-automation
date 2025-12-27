import json
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi import Body

from app.db import SessionLocal
from app.models import Job, JobStatus
from app.sqs_client import send_job_to_queue

from fastapi import APIRouter
from worker.jira.jira_client import create_jira_ticket

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs")
def create_job(data: dict, db: Session = Depends(get_db)):

    if data["type"] == "zoom" and "zoom.us" not in data["source_url"]:
        raise HTTPException(status_code=400, detail="Invalid Zoom URL")
    
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

    return {
        "job_id": job.job_id,
        "status": job.status,
        "result": job.result,
        "jira_tickets": json.loads(job.jira_tickets) if job.jira_tickets else []
    }


@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.job_id.desc()).all()

    return [
        {
            "job_id": j.job_id,
            "source_url": j.source_url,
            "status": j.status,
        }
        for j in jobs
    ]



@router.post("/jobs/{job_id}/jira")
def create_jira(job_id: str, items: list = Body(...), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()

    created = []

    for item in items:
        issue = create_jira_ticket(
            title=item["title"],
            description=item["description"],
            priority=item["priority"]
        )

        created.append({
            "key": issue["key"],
            "url": f"{os.getenv('JIRA_BASE_URL')}/browse/{issue['key']}"
        })

    job.jira_tickets = json.dumps(created)
    db.commit()

    return {"jira_tickets": created}
