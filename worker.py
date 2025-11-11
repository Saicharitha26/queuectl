import subprocess
import time
from rich.console import Console
from .job_manager import get_next_job, update_job, move_to_dlq
from .config import load_config

console = Console()

def start_worker(worker_id=1):
    config = load_config()
    console.print(f"[bold blue]Worker-{worker_id} started[/bold blue]")
    while True:
        job = get_next_job()
        if not job:
            time.sleep(2)
            continue
        console.print(f"[cyan]Worker-{worker_id} processing job {job['id']}[/cyan]")
        try:
            result = subprocess.run(job["command"], shell=True)
            if result.returncode == 0:
                update_job(job["id"], {"state": "completed"})
                console.print(f"[green]Job {job['id']} completed successfully[/green]")
            else:
                handle_failure(job, config)
        except Exception as e:
            console.print(f"[red]Error running job {job['id']}: {e}[/red]")
            handle_failure(job, config)

def handle_failure(job, config):
    job["attempts"] += 1
    max_retries = job.get("max_retries", config["max_retries"])
    base = config["backoff_base"]

    if job["attempts"] > max_retries:
        job["state"] = "dead"
        move_to_dlq(job)
        console.print(f"[red]Job {job['id']} moved to DLQ[/red]")
    else:
        delay = base ** job["attempts"]
        console.print(f"[yellow]Retrying job {job['id']} after {delay}s[/yellow]")
        time.sleep(delay)
        job["state"] = "pending"
        update_job(job["id"], job)
