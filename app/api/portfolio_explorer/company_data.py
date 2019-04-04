from iexfinance.stocks import Stock
import os

class CompanyData():

    def __init__(self, ticker):
        # add these two to app/__init__.py
        os.environ['IEX_API_VERSION'] = 'iexcloud-beta'
        os.environ['IEX_AUTH_TOKEN'] = 'pk_172a73e7b4554b7ba9f06ebbad793dd3'

        stock = Stock(ticker)
        self.time 
        self.peers = stock.get_peers()
        # what is market price? do you mean current price of a single stock?
        self.shares_outstanding = stock.get_shares_outstanding()
        self.market_cap = stock.get_market_cap()

        balance_sheet = stock.get_balance_sheet()['balancesheet'][0]
        self.equity = balance_sheet['shareholderEquity']
        self.debt = balance_sheet['longTermDebt']
        self.total_current_assets = balance_sheet['currentAssets']
        self.total_current_liabilities = balance_sheet['totalCurrentLiabilities']

        income_statement = stock.get_income_statement()['income'][0]
        self.net_income = income_statement['netIncome']
        # what are:
        #     'operatingActivities':None, do you mean operatingIncome from income statement?
        #     'investingActivities':None, do you mean totalInvestingCashFlows from cash flow statement?
        #     'financingActivities':None, do you mean cashFlowFinancing from cash flow statement?
        
        self.debt_equity_ratio = self.total_current_liabilities / self.equity # online definition, you wrote it as debt/equity
        self.book_value = self.equity / self.shares_outstanding # your definition
        self.earnings_per_share = stock.get_latest_eps() # directly from IEX
        self.pe_ratio = None # depends on market price
        self.pbvRation = None # depends on market price
        self.risk = None # depends on market price
        self.margin_of_safety = None # depends on market price
        self.current_ratio = self.total_current_assets / self.total_current_liabilities



