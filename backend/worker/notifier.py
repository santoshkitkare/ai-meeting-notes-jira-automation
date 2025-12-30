import requests

def notify_progress(job_id, status, progress=0, message=None, result=None):
    try:
        requests.post(
            "http://localhost:8000/internal/notify",
            json={
                "job_id": job_id,
                "status": status,
                "progress": progress,
                "message": message,
                "result": result
            },
            timeout=10
        )
    except Exception as e:
        print("⚠️ Notify failed:", e)
