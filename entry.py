from app import app

print("Server startup ...")

from app.models import *

snp500_tickers.initialize()

from apscheduler.schedulers.background import BackgroundScheduler
from startup_tasks import cache_data

scheduler = BackgroundScheduler()
scheduler.add_job(func=cache_data, trigger="interval", seconds=10)
scheduler.start()
