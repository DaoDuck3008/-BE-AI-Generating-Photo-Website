from typing import Dict

# In-memory job store to keep track of job statuses and details
JOB_STORE: Dict[str, Dict] = {}

def create_job(job_id: str):
    JOB_STORE[job_id] = {
        "status": "processing",
        "step": "init",
        "progress": 0,
        "message": "Khởi tạo"
    }

def update_job(
        job_id: str,
        *,
        status: str = None,
        step: str = None,
        progress: int = None,
        message: str = None
):
    if job_id not in JOB_STORE:
        return
    
    job = JOB_STORE[job_id]

    if status is not None:
        job["status"] = status
    if step is not None:
        job["step"] = step
    if progress is not None:
        job["progress"] = progress
    if message is not None:
        job["message"] = message
