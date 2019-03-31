from app.models import Task
from app import app


def launch_task(name, stock_ticker, *args, **kwargs):
    rq_job = app.snp500_data_queue.enqueue('app.api.tasks.' + name, stock_ticker, *args, **kwargs)
    task = Task(job_id= rq_job.get_id(), name=name)
    task.save()

    return task