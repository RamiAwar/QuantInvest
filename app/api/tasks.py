from app import app
from rq import get_current_job
from app.models import Task, StockDailyPrice
from app.api.stock_prices.get_data import fetch_missing_data
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import sys
from app.models import StockDailyPrice


app.app_context().push()

def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')

def fetch_snp500_data(stock_tickers):
    try:
        current_date = datetime.now()
        missing_data = fetch_missing_data(stock_tickers, current_date-relativedelta(years=5), current_date)
        for quote in missing_data:
            stockDailyPrice = StockDailyPrice(stock_ticker=quote['stock_ticker'], date=quote['date'], price=quote['price'])
            stockDailyPrice.save()
    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())