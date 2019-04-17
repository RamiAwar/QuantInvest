

from app.api.backtest.get_statistics import *
from flask import Blueprint
from datetime import datetime

bp = Blueprint('backtest', __name__)


def backtest_portfolio(prices_df, portfolio, initial_amount, window):
    """Returns backtested portfolio dataframe, along with moving average and moving standard deviation rolling statistics using window specified.

    Arguments:
            prices_df {Pandas dataframe} -- Dataframe containing timestamped stock prices, columns are stock tickers, rows timestamps
            portfolio {dict} -- Dictionary containing stock tickers as keys, percentage allocations as values
            initial_amount {int} -- Initial portfolio net worth or investment
            window {int} -- Window for computing rolling statistics on portfolio backtested results

    Returns:
            Pandas dataframe -- Dataframe containing total portfolio values, moving average, and moving standard deviations
            """
    performance = compute_statistics(prices_df, initial_amount, portfolio, window)

    return performance
