import uuid
from .storage import load_jobs, save_jobs, load_dlq, save_dlq
from .utils import current_time

def enqueue_job(data):
    jobs = load_jobs()
    job_id = data.get("id", str(uuid.uuid4()))
    job = {
        "id": job_id,
        "command": data.get("command"),
        "state": "pending",
        "attempts": 0,
        "max_retries": data.get("max_retries", 3),
        "created_at": current_time(),
        "updated_at": current_time()
    }
    jobs.append(job)
    save_jobs(jobs)
    return job

def get_next_job():
    jobs = load_jobs()
    for job in jobs:
        if job["state"] == "pending":
            job["state"] = "processing"
            save_jobs(jobs)
            return job
    return None

def update_job(job_id, updates):
    jobs = load_jobs()
    for job in jobs:
        if job["id"] == job_id:
            job.update(updates)
            job["updated_at"] = current_time()
            save_jobs(jobs)
            return job
    return None

def move_to_dlq(job):
    dlq = load_dlq()
    dlq.append(job)
    save_dlq(dlq)
    jobs = [j for j in load_jobs() if j["id"] != job["id"]]
    save_jobs(jobs)
