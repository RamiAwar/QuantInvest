# functions to be used by the financial database component

import numpy as np
import pandas as pd
import requests
import json


class Company():

    historical_prices = {}
    balance_sheet = {}
    financials = {}
    key_stats = {}
    peers = {}
    # ...

    def __init__ (self):
        pass

    # return company symbol from company name. could be improved to work with partial string matching, and name suggestions
    def getSymbol(self, symbols, name):
        for item in symbols:
            if (item['name'] == name):
                return(item['symbol'])

    def getRequest(self, path, apiKey):
        return(requests.get('https://cloud.iexapis.com/beta/' + path + '?token=' + apiKey))

    def update(self):
        historical_prices = getRequest(self, '/stock/aapl/chart/2y', 'pk_a91586fc254847e08b030f86765dabaf')


# return rolling correlation of two time-series vectors for specified window size
def rollingCorr(self, x, y, window):
    return(x.rolling(window).corr(y))


############## TEST ##############
def pimple(self):
    print("modified pimple")
