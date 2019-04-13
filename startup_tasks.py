from app.models import StockDailyPrice, snp500_tickers
from app.api.stock_fetcher.launch_task import launch_task
from datetime import datetime
from dateutil.relativedelta import relativedelta

def cache_data():

    snp_500_tickers = snp500_tickers.objects.all()
    snp_500_tickers = [ticker.symbol for ticker in snp_500_tickers]
    
    current_date = datetime.now()

    default_date = current_date - relativedelta(years=5)
    latest_available_data = StockDailyPrice.objects.order_by('-date').first()

    if latest_available_data != None:
        latest_available_date = latest_available_data.date
    else:
        latest_available_date = default_date

    for i in range(0, len(snp_500_tickers), 100):
        task = launch_task('fetch_snp500_data', list(snp_500_tickers[i:i + 100]), latest_available_date, current_date)
