import pandas as pd
from dateutil.relativedelta import relativedelta

from iexfinance.stocks import get_historical_data

from app import snp_500_df
from app.models import StockDailyPrice
from app.api.stock_fetcher.daily_price_dto import DailyPriceDto
from app.models import StockDailyPrice


def get_all_snp500_data(start_date, end_date):

    data = StockDailyPrice.objects(date__lte=end_date, date__gte=start_date)
    
    data_df = pd.DataFrame()
    data_df['date'] = pd.date_range(start_date, end_date)
    data_df = data_df.set_index(['date'])
    
    for stock_ticker in snp_500_df['Symbol']:
        data_df[stock_ticker] = float('nan')
    
    for quote in data:
        data_df.at[quote.date, quote.stock_ticker] = quote.price
    
    data_df.dropna(how='all', inplace=True)
    
    return data_df

def fetch_missing_data(stock_tickers, start_date, end_date):
    
    if len(stock_tickers) == 1:
    
        missing_data = {}
    
        stock_data = get_historical_data(stock_tickers, start_date, end_date)
        stock_data = [DailyPriceDto(stock_tickers, value['open'], key).to_dict() for key, value in stock_data.items()]
    
        if len(stock_data) == 0:
            return {}
    
        missing_data[stock_tickers[0]] = stock_data
        return missing_data
    
    else:
    
        missing_data = {}
    
        for i in range(0, len(stock_tickers), 100):
    
            stock_data = get_historical_data(stock_tickers[i:i+100], start_date, end_date)
            current_data = {}
    
            for ticker, quote in stock_data.items():
                ticker_data = []
    
                for date, prices in quote.items():
                    ticker_data.append(DailyPriceDto(ticker, prices['open'], date).to_dict())
    
                current_data[ticker] = ticker_data
    
            missing_data.update(current_data)
    
        return missing_data

def get_data(stock_tickers, start_date, end_date):
    """Fetch ticker data for given list of tickers, from start date to end date
    
    Splits ticker list into snp500 stocks and non-snp500 stocks to use cache database 
    for quicker results.
    
    Arguments:
        stock_tickers {list} 
        start_date {datetime} 
        end_date {datetime} 
    
    Returns:
        dictionary -- Dictionary keys tickers, values are points on portfolio timeline
    """
    
    # Split ticker list into snp500 tickers and non-snp500 tickers
    snp_500_tickers = [ticker for ticker in stock_tickers if ticker in snp_500_df['Symbol']] # this list contains all the snp_500 tickers from the input
    not_snp_500_tickers = [ticker for ticker in stock_tickers if ticker not in snp_500_tickers] # this list contains all the other tickers
    
    stock_data = {} # this dict will contain all the retrieved data
    
    for stock_ticker in snp_500_tickers:
        data = StockDailyPrice.objects(stock_ticker=stock_ticker, date__lte=end_date, date__gte=start_date)
        data = [ DailyPriceDto(stock_ticker, quote.date, quote.price).to_dict() for quote in data ]
        stock_data[stock_ticker] = data
    

    not_snp_500 = fetch_missing_data(not_snp_500_tickers, start_date, end_date)
    
    stock_data.update(not_snp_500) # combines the two dictionaries
    
    return stock_data

