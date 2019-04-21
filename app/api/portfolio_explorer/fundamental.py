# this class contains functions for fundamental analysis of companies.
# TODO:
# include a function for the four fundamental rules of warren buffett:

from company_data import CompanyData
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

class Fundamental():

    def __init__(self, stock, period):
        self.company_data = CompanyData(stock, period, False) # get the data for the company withint the period ('quarterly' or 'annually')

    def get_all_data(self):
        # Make it return a dictionary of all the data we need. Add calls to all the other methods to fill the dictionary
        pass

    # calculate intrinsic value of a company
    def intrinsicValue(self, companyData, interestRate, years):

        bv = []
        fin = companyData['financials_over_time']

        for key in fin:
            bv.append(fin[key]['book_value'])

        # first check stability of book value growth
        lr = lineReg(companyData, 'book_value')

        if(lr[2] < 0.9):
            print('The company book value is not stable enough for intrinsic value to be calculated.')
            return(-1)

        # if growth is stable, find average percent change in book value over last 4 years
        meanBVChange = np.mean([bv[i+1]/bv[i]-1 for i in range(len(bv)-1)])  # mean change in book value
        BV = bv[len(bv)-1]
        meanDiv = np.mean(companyData['dividends'])

        IV = (BV*(1+meanBVChange)^years + years*meanDiv)/(1+interestRate)^years

        return(IV)


    # return assessment of stability of desired variable based on r squared of past 4 years. variable is one of:
    # equity
    # debt
    # total_assets
    # total_liabilities
    # debt_equity_ratio
    # book_value
    # pbv_ratio
    # risk
    # margin_of_safety
    # current_ratio
    def lineReg(self, companyData, variable):
        fin = data["financials_over_time"]
        x = []
        y = []

        if(fin[key].get(variable, None) == None):
            print('key error:' + variable + 'is not a valid variable')
            return(-1)

        for key in fin:
            date = datetime.fromisoformat(key).timestamp()
            x.append(date)
            y.append(fin[key][variable])

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        out = [slope, intercept, r_value, p_value, std_err]

        return(out)


    # return an overview of the health and fundamentals of a company
    def health(self, companyData):  # call this health

        fin = companyData['financials_over_time']

        pbv = []
        de = []
        curr = []
        intval = []

        for key in fin:
            pbv.append(fin[key]['pbv_ratio'])
            de.append(fin[key]['debt_equity_ratio'])
            curr.append(fin[key]['current_ratio'])

        to_return = {
        'pbv_ratio': pbv,
        'debt_equity_ratio': de,
        'intrinsic_value': intval,
        'current_ratio': curr
        }

        return to_return

    # returns a quick assessment of cash flow history. checks if operating activities are positive,
    # finance and investing activities are negative, if growth is stable, and if cash flow is increasing.
    # if details == TRUE, more details are given.
    def cashFlowHistory(self, companyData, details):
        pass

    # returns a forecast of the desired variable for a number of years into the future.
    # prints warning if variable is unstable over the period of past available data.
    def forecast(self, companyData, variable):
        pass

    # compare a company's returns with a bond's returns
    def compareBond(self, companyData):
        pass

    # compare two companies in terms of debtEquityRatio, and other things.
    def compare(self, companyData1, companyData2, var):
        pass

    # return a quick assessment of equity per share stability over last 10 years
    # if details == TRUE, more details are given.
    def equityPerShareHist(self, companyData, details):
        pass

    # return a quick assessment of debt per equity stability over last 10 years
    # if details == TRUE, more details are given.
    def debtPerEquityHist(self, companyData, details):
        pass

    # return a quick assessment of earnings stability over last 10 years
    # if details == TRUE, more details are given.
    def earningsHist(self, companyData):
        pass

    # returns the average P/E ratio of the market, or a sector
    def sectorPE(self, data):
        pass

    # get the current interest rate
    def interestRate(self):
        pass
