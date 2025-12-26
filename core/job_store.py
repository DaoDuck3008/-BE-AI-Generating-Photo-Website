import uuid 
import json
from utilities.redis_client import redis_client

def create_job():
    job_id = str(uuid.uuid4()) # tạo mã jobID

    job_data = { 
        "status": "pending",
        "step": "",
        "progress": 0,
        "message": ""
    }

    redis_client.set(job_id, json.dumps(job_data), ex= 180)
    return job_id

def update_job(job_id, **kwargs):
    job = json.loads(redis_client.get(job_id))

    job.update(kwargs)
    redis_client.set(job_id, json.dumps(job))