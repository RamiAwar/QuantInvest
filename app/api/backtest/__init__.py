from flask import Blueprint
from datetime import datetime 

bp = Blueprint('backtest', __name__)

from app.api.backtest import routes

from app.api.backtest.get_statistics import (prepare_dataframe, 
                                            compute_statistics, 
                                            compute_daily_returns,
                                            compute_moving_average,
                                            compute_moving_standard_deviation)


def get_daily_returns(portfolio, start_date, end_date):
	
    prices_df = prepare_dataframe(portfolio, 
    								datetime.strptime(start_date, '%Y-%m-%d'), 
                                    datetime.strptime(end_date, '%Y-%m-%d'))

    performance = compute_daily_returns(prices_df)

    return performance
