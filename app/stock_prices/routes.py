"""
.. module:: main
   :synopsis: All endpoints getting the historical data are defined here
.. moduleauthor:: Nader Al Awar <github.com/naderalawar>
"""

from app.stock_prices import bp
from flask import request
from app.stock_prices.get_data import get_data
from flask import jsonify
from datetime import datetime

@bp.route("/", methods=['GET'])
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
            
            GET http://127.0.0.1:5000/stock_prices/?ticker=GOOG&start=01052018&end=05052018
        
         - Expected Success Response::

            [
                {
                    "close_price":558.46,
                    "date":"Thu, 01 May 2014 00:00:00 GMT",
                    "highest_price":568.0,
                    "lowest_price":552.92,
                    "open_price":568.0,
                    "stock_ticker":"GOOG",
                    "volume":13052.0
                },
                {

                },
            ]
    """
    stock_ticker = request.args.get('ticker')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    start_date = datetime.strptime(start_date, '%d%m%Y')
    end_date = datetime.strptime(end_date, '%d%m%Y')

    return jsonify(get_data(stock_ticker, start_date, end_date))