from app.models import StockDailyPrice, snp500_tickers
from app.api.stock_fetcher.launch_task import launch_task


def cache_data():

    if StockDailyPrice.objects.first() == None:  # check if any data for any snp 500 stock exists

        snp_500_tickers = snp500_tickers.objects.all()
        snp_500_tickers = [ticker.symbol for ticker in snp_500_tickers]

        for i in range(0, len(snp_500_tickers), 100):
            task = launch_task('fetch_snp500_data', list(snp_500_tickers[i:i + 100]))
