# this class contains functions for fundamental analysis of companies.

from company_data import CompanyData
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

class Fundamental():

    def __init__(self, stock, period):
        self.company_data = CompanyData(stock, period, False) # get the data for the company withint the period ('quarterly' or 'annually')

    def get_all_data(self):
        # Make it return a dictionary of all the data we need. Add calls to all the other methods to fill the dictionary
        to_return = {
        'health':
        }

    # find peers of a company (either asks the db or gets them itself)
    def peers(self, companyData, criterion):
        pass

    # calculate intrinsic value of a company (simliar to buffettsbooks.com calculator)
    def intrinsicValue(self, companyData, interestRate):
        pass

    # returns important indicators about a company for quick assessment
    def indicators(self, companyData):
        pass

    # ask the database for default rate of company
    def defaultRate(self, companyData):
        pass

    # return assessment of stability of desired variable based on MSE past 10 years. variable must be string
    def stability(self, companyData, variable):
        pass

    # return an overview of the health and fundamentals of a company
    def health(self, companyData):  # call this health

        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # data = companyData['financials_over_time']
        #
        # der = []
        # pbv = []
        # cr = []
        # dates = []
        #
        # for key in data:
        #     der.append(data[key]['debt_equity_ratio'])  # <0.5
        #     pbv.append(data[key]['pbv_ratio'])          # <1.5
        #     cr.append(data[key]['current_ratio'])       # <1.5
        #     dates.append(key)
        #
        # ax.scatter(der, pbv, cr)
        #
        # ax.set_xlabel('Debt to Equity Ratio')
        # ax.set_ylabel('Price to Book Value Ratio')
        # ax.set_zlabel('Current Ratio')
        #
        # for i, txt in enumerate(dates):
        #     ax.text(der[i], pbv[i], cr[i], dates[i])
        #
        # v = np.array([[0, 0, 0], [0, 0, 0.5], [1, 1, -1],  [-1, 1, -1], [0, 0, 1]])
        # ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])
        #
        # # generate list of sides' polygons of our pyramid
        # verts = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]],[v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]
        #
        # # plot sides
        # ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
        #
        # plt.show()

        # if(np.any(companyData['debtEquityRadio'] > 0.5)):
        #     print('Your company has a significant amount of debt. You might want to check its cash flow statement.')
        # if(np.any(companyData['peRatio'] > 15)):
        #     print('Your company could be over valued. You might want to check its instrinsic value.')
        # if(np.any(companyData['currentRatio'] > 1.5)):
        #     print('Your company has too many liabilities. You might want to check its balance sheet.')



    # returns a quick assessment of cash flow history. checks if operating activities are positive,
    # finance and investing activities are negative, if growth is stable, and if cash flow is increasing.
    # if details == TRUE, more details are given.
    def cashFlowHistory(self, companyData, details):
        pass


    # returns a forecast of the desired variable for a number of years into the future.
    # prints warning if variable is unstable over the period of past available data.
    def forecast(self, companyData):
        pass

    # have the management of this company led companies that defaulted in the past?
    def management(self, companyData):
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

    # forecast a variable x years into the future (linear forecasting)
    # return -1 if variable too volatile
    def forecast(self, companyData):
        pass

    # returns the average P/E ratio of the market, or a sector
    def averagePE(self, data):
        pass

    # get the current interest rate
    def interestRate(self):
        pass
