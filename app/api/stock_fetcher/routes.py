"""
.. module:: main
   :synopsis: All endpoints getting the historical data are defined here
.. moduleauthor:: Nader Al Awar <github.com/naderalawar>
"""

from app.api.stock_fetcher import bp
from flask import request
from app.api.stock_fetcher.get_data import get_data
from flask import jsonify
from datetime import datetime

@bp.route("/", methods=['POST'])
def get_stock_ticker_data():
    """
        **Get the historical data**

        This function allows the user to get the historical data of a stock between two dates

        :param ticker: ticker of the stock
        :param start: starting point of the data in DDMMYYY format
        :param end: end point of the data in DDMMYYY format
        :type ticker: int
        :return: json of historical data 

        - Example ::
            
            POST http://127.0.0.1:5000/api/stock_prices/?ticker=GOOG&start=01052018&end=05052018
            '{
                "Tickers": ['AAPL', 'TSLA'],
                "Start": 01052018,
                "End": 05052018
            }'
        
         - Expected Success Response::

    """
    data_requested = request.get_json(force=True)
    stock_tickers = data_requested['Tickers']
    start_date = data_requested['Start']
    end_date = data_requested['End']
    start_date = datetime.strptime(start_date, '%d%m%Y')
    end_date = datetime.strptime(end_date, '%d%m%Y')

    return jsonify(get_data(stock_tickers, start_date, end_date))