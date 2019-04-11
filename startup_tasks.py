from app.models import StockDailyPrice, SnP500Tickers
from app.api.stock_fetcher.launch_task import launch_task

def cache_data():

        print("caching data")
        
        snp_500_tickers = SnP500Tickers.objects.all()
        snp_500_tickers = [ticker.symbol for ticker in snp_500_tickers]

        for i in range(0, len(snp_500_tickers), 100):
            task = launch_task('fetch_snp500_data', list(snp_500_tickers[i:i+100]))