import pandas as pd
from app.api.stock_prices.get_data import get_data
from app.api.backtest.data_manipulation import dict_to_dataframe

def prepare_dataframe(portfolio, start_date, end_date):
    # portfolio is a dict mapping stocks to weights
    stock_prices = {}

    for key, value in portfolio.items():
        stock_prices[key] = get_data(key, start_date, end_date)
    
    df = dict_to_dataframe(stock_prices)
    df.dropna(inplace=True)
    df = compute_total_value(df, portfolio)

    return df

def compute_total_value(prices_over_time, portfolio):
    df = prices_over_time
    for column in df:
        df[column] = df[column].apply(lambda x: x * portfolio[column]) # multiply each column by the number of stocks bought to get total price
    stocks_list = list(df)
    df['total_value'] = df.sum(axis=1)
    df.drop(stocks_list, axis=1, inplace=True)
    return df

def compute_daily_returns(prices_over_time):
    df = prices_over_time
    df['daily_returns'] = df.pct_change()
    return df

def compute_moving_average(prices_over_time, window):
    df = prices_over_time
    df['moving_average'] = float('nan')
    df['moving_average'] = df.rolling(window=window).mean()
    return df

def compute_moving_standard_deviation(prices_over_time, window):
    df = prices_over_time
    df['moving_standard_deviation'] = float('nan')
    df['moving_standard_deviation'] = df.rolling(window=window).std()
    return df

def compute_statistics(prices_over_time):
    df = prices_over_time
    df = compute_daily_returns(df)
    df = compute_moving_average(df, 50)
    df = compute_moving_standard_deviation(df, 50)
    return df    