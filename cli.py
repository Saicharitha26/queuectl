import json
import click
import multiprocessing
from rich.console import Console
from .job_manager import enqueue_job
from .worker import start_worker
from .config import load_config, update_config
from .storage import load_jobs
from .dlq_manager import list_dlq, retry_from_dlq

console = Console()

@click.group()
def cli():
    """QueueCTL - Background Job Queue CLI"""
    pass

@cli.command()
@click.argument("job_json")
def enqueue(job_json):
    """Add a new job"""
    job_data = json.loads(job_json)
    job = enqueue_job(job_data)
    console.print(f"[green]Enqueued job:[/green] {job['id']}")

@cli.command()
@click.option("--count", default=1, help="Number of workers to start")
def worker(count):
    """Start workers"""
    for i in range(count):
        p = multiprocessing.Process(target=start_worker, args=(i+1,))
        p.start()

@cli.command()
@click.option("--state", default=None, help="Filter jobs by state")
def list(state):
    """List jobs"""
    jobs = load_jobs()
    if state:
        jobs = [j for j in jobs if j["state"] == state]
    for job in jobs:
        console.print(job)

@cli.command()
def dlq():
    """List DLQ jobs"""
    for job in list_dlq():
        console.print(job)

@cli.command()
@click.argument("job_id")
def retry(job_id):
    """Retry a job from DLQ"""
    job = retry_from_dlq(job_id)
    if job:
        console.print(f"[green]Job {job_id} retried successfully[/green]")
    else:
        console.print(f"[red]Job {job_id} not found in DLQ[/red]")

@cli.command()
@click.argument("key")
@click.argument("value")
def config(key, value):
    """Update configuration"""
    update_config(key, int(value))
    console.print(f"[blue]Updated config:[/blue] {key} = {value}")

@cli.command()
def showconfig():
    """Show current configuration"""
    console.print(load_config())

if __name__ == "__main__":
    cli()
