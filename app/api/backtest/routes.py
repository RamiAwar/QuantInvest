"""
.. module:: BackTesting
   :synopsis: Backtests a portfolio based on historical data 
.. moduleauthor:: Nader Al Awar <github.com/naderalawar>
"""

from app.api.backtest import bp

import pandas as pd
from flask import request
from flask import jsonify

from app.api.backtest.get_statistics import prepare_dataframe
from app.api.backtest.get_statistics import compute_statistics
from app.api.backtest.get_statistics import compute_daily_returns
from app.api.backtest.get_statistics import compute_moving_average
from app.api.backtest.get_statistics import compute_moving_standard_deviation

from datetime import datetime

@bp.route("/", methods=['POST'])
def get_portfolio_statistics():
    """
        **Gets all portfolio statistics: daily returns, moving_average, moving_standard_deviation.**
        This function allows user to get the results of a portfolio when backtested on historical data. Note that the first few 
        entries for daily_returns, moving_average, and moving standard_deviation will be null.
        :param start: starting point of the data in DDMMYYY format
        :param end: end point of the data in DDMMYYY format
        :return: results of the backtest
        - Example::
            POST http://127.0.0.1:5000/backtest/?window=50&start=01012018&end=05012018
            '{
                "AAPL": 2,
                "TSLA": "7"
            }'
        - Expected Success Response::
            {
                "1403481600000":
                {
                    "total_value":1827.6768,
                    "daily_returns":53.2628,
                    "moving_average":1595.504664,
                    "moving_standard_deviation":90.1876341337
                },
                "1403568000000":
                {
                    "total_value":1793.6248,
                    "daily_returns":-34.052,
                    "moving_average":1600.118304,
                    "moving_standard_deviation":94.2947709698
                },
            }
    """
    portfolio = request.get_json(force=True)

    try:
        window = int(request.args.get('window'))
    except:
        pass

    start_date = parse_date(request.args.get('start'))
    end_date = parse_date(request.args.get('end'))
    prices_df = prepare_dataframe(portfolio, start_date, end_date)

    performance = compute_statistics(prices_df)
    return performance.to_json(orient='index')

@bp.route("/daily_returns", methods=['POST'])
def get_daily_returns():
    """
        **Gets all the daily returns of a portfolio.**
        This function allows user to get the daily returns of a portfolio when backtested on historical data. The first entry for
        daily_returns is null.
        :param start: starting point of the data in DDMMYYY format
        :param end: end point of the data in DDMMYYY format
        :return: results of the backtest
        - Example::
            POST http://127.0.0.1:5000/backtest/daily_returns?start=01012018&end=05012018
            '{
                "AAPL": 2,
                "TSLA": "7"
            }'
        - Expected Success Response::
            {
                "1403481600000":
                {
                    "total_value":1827.6768,
                    "daily_returns":53.2628,
                },
                "1403568000000":
                {
                    "total_value":1793.6248,
                    "daily_returns":-34.052,
                },
            }
    """
    portfolio = request.get_json(force=True)
    start_date = parse_date(request.args.get('start'))
    end_date = parse_date(request.args.get('end'))

    prices_df = prepare_dataframe(portfolio, start_date, end_date)
    performance = compute_daily_returns(prices_df)

    return performance.to_json(orient='index')

@bp.route("/moving_average", methods=['POST'])
def get_moving_average():
    """
        **Gets all the computed moving average values of a portfolio.**
        This function allows user to get the moving average values of a portfolio when backtested on historical data.
        The user can optionally define the window parameter (the default is 50). The first number of entries equal
        to the window size is null.
        :param window: the window size for computing average and std_dev
        :param start: starting point of the data in DDMMYYY format
        :param end: end point of the data in DDMMYYY format
        :return: results of the backtest
        - Example::
            POST http://127.0.0.1:5000/backtest/daily_returns?window=50&start=01012018&end=05012018
            '{
                "AAPL": 2,
                "TSLA": "7"
            }'
        - Expected Success Response::
            {
                1402531200000":
                {
                    "total_value":1827.6768,
                    "moving_average":1581.275272
                },
            }
    """
    portfolio = request.get_json(force=True)
    try:
        window = int(request.args.get('window'))
    except:
        pass
    start_date = parse_date(request.args.get('start'))
    end_date = parse_date(request.args.get('end'))
    print(start_date)
    print(end_date)

    prices_df = prepare_dataframe(portfolio, start_date, end_date)
    performance = compute_moving_average(prices_df, window)
    return performance.to_json(orient='index')

@bp.route("/moving_standard_deviation", methods=['POST'])
def get_moving_standard_deviation():
    """
        **Gets all the computed moving standard deviation values of a portfolio.**
        This function allows user to get the moving standard deviation values of a portfolio when backtested on historical data.
        The user can optionally define the window parameter (the default is 50). The first number of entries equal
        to the window size is null.
        :param window: the window size for computing average and std_dev
        :param start: starting point of the data in DDMMYYY format
        :param end: end point of the data in DDMMYYY format
        :return: results of the backtest
        - Example::
            POST http://127.0.0.1:5000/backtest/daily_returns?window=50&start=01012018&end=05012018
            '{
                "AAPL": 2,
                "TSLA": "7"
            }'
        - Expected Success Response::
            {
                1403481600000":
                {
                    "total_value":1594.4634,
                    "moving_standard_deviation":90.1876341337
                },
            }
    """
    portfolio = request.get_json(force=True)
    try:
        window = int(request.args.get('window'))
    except:
        pass
    start_date = parse_date(request.args.get('start'))
    end_date = parse_date(request.args.get('end'))
    prices_df = prepare_dataframe(portfolio, start_date, end_date)

    performance = compute_moving_standard_deviation(prices_df, window)
    
    return performance.to_json(orient='index')

def parse_date(date):

    return datetime.strptime(date, '%d%m%Y')

