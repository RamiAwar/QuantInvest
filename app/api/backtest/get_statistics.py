import pandas as pd
from app.api.stock_fetcher.get_data import get_data
from app.api.backtest.data_manipulation import dict_to_dataframe


def prepare_dataframe(portfolio, start_date, end_date):

    # portfolio is a dict mapping stocks to weights
    # print(portfolio.keys())
    # print(portfolio)

    df = get_data(list(portfolio.keys()), start_date, end_date)
    df.dropna(inplace=True)

    return df


def compute_total_value(prices_df, initial_amount, portfolio):

    # Get portfolio data
    # prices_df = get_historical_data(list(portfolio.keys()), output_format="pandas")
    # db['AAPL']['Adj. Close'].diff()

    prices_df = pd.concat([(prices_df[stock].diff() + initial_amount) * portfolio[stock]
                           for stock in list(portfolio.keys())], axis=1, keys=list(portfolio.keys())).sum(axis=1).dropna()
    prices_df = prices_df.drop(prices_df.index[0])
    return prices_df


def compute_daily_returns(prices_over_time):
    df = prices_over_time
    df['daily_returns'] = df.pct_change()
    df.dropna(inplace=True)
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
