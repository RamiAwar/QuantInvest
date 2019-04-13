from app.models import Task
from app import app


def launch_task(name, stock_ticker, *args, **kwargs):

    # Launch task with name == name
    rq_job = app.snp500_data_queue.enqueue('app.api.tasks.' + name, stock_ticker, *args, job_timeout=999999, **kwargs)

    # Save task in database
    task = Task(job_id=rq_job.get_id(), name=name)
    task.save()

    return task
