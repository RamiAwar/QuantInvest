from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
import json

from app import app
from app.models import User, snp500_tickers
from app.explorer import bp


@bp.route('/stock', methods=["GET"])
@login_required
def stockexplorer():
    
    ticker = request.args.get("ticker").upper();
    print(ticker)
    return render_template('explorer/stock_explorer.html', ticker=ticker)


@bp.route("/search")
def search():

    text = request.args['searchText'] # get the text to search for

    # create an array with the elements of BRAZIL_STATES that contains the string
    # the case is ignored
    stocks = list(snp500_tickers.objects())

    # TODO: Find solution for adding all stocks to search result : priority (3)
    # Manually added stocks for demo
    stocks.append(snp500_tickers(name="Tesla", symbol="TSLA"));

    result = [c.symbol for c in stocks if (text.upper() in c.name.upper() or text.upper() in c.symbol.upper())]

    
    # return as JSON
    return json.dumps({"results":result}) 