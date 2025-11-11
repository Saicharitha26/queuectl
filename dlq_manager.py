from .storage import load_dlq, save_dlq, load_jobs, save_jobs
from .utils import current_time

def list_dlq():
    return load_dlq()

def retry_from_dlq(job_id):
    dlq = load_dlq()
    for job in dlq:
        if job["id"] == job_id:
            job["state"] = "pending"
            job["attempts"] = 0
            job["updated_at"] = current_time()
            jobs = load_jobs()
            jobs.append(job)
            save_jobs(jobs)
            dlq = [j for j in dlq if j["id"] != job_id]
            save_dlq(dlq)
            return job
    return None
