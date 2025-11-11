import json
import os

JOB_FILE = "jobs.json"
DLQ_FILE = "dlq.json"

def _init_files():
    for file in [JOB_FILE, DLQ_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump([], f)

def load_jobs():
    _init_files()
    with open(JOB_FILE, "r") as f:
        return json.load(f)

def save_jobs(jobs):
    with open(JOB_FILE, "w") as f:
        json.dump(jobs, f, indent=4)

def load_dlq():
    _init_files()
    with open(DLQ_FILE, "r") as f:
        return json.load(f)

def save_dlq(dlq):
    with open(DLQ_FILE, "w") as f:
        json.dump(dlq, f, indent=4)
