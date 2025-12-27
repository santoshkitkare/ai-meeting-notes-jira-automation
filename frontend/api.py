import requests
from config import BACKEND_URL


def create_job(source_url, source_type):
    res = requests.post(
        f"{BACKEND_URL}/jobs",
        json={
            "source_url": source_url,
            "type": source_type
        }
    )
    return res.json()


def get_job_status(job_id):
    res = requests.get(f"{BACKEND_URL}/jobs/{job_id}")
    return res.json()


def get_all_jobs():
    res = requests.get(f"{BACKEND_URL}/jobs")
    return res.json()
