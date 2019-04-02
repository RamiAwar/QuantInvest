

from app.api.backtest.get_statistics import *
from flask import Blueprint
from datetime import datetime

bp = Blueprint('backtest', __name__)


def backtest_portfolio(prices_df, portfolio, initial_amount, start_date, end_date):

    performance = compute_total_value(prices_df, initial_amount, portfolio)

    return performance
