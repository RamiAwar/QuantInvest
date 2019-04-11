from app import app

print("Server startup ...")

from app.models import *

snp500_tickers.initialize()

from apscheduler.schedulers.background import BackgroundScheduler
from startup_tasks import cache_data
from datetime import datetime

print("TEST)")

scheduler = BackgroundScheduler()
scheduler.add_job(func=cache_data, trigger="interval", days=1)
scheduler.start()
for job in scheduler.get_jobs():
    job.modify(next_run_time=datetime.now())
