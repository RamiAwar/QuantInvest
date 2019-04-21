from iexfinance.stocks import Stock
import os

class CompanyData():

    def fetch_data(self, ticker, period):
        stock = Stock(ticker)
        self.peers = stock.get_peers()
        self.__key_stats = stock.get_key_stats(period=period)
        self.__financials = stock.get_financials(period=period) # set the period. default is quarterly
        self.__dividends = stock.get_dividends('5y')

        if self.__cloud == True:
            self.__income_statements = stock.get_income_statement(period=period)['income']
            self.__cash_flow_statements = stock.get_cash_flow(period=period)['cashflow']

        self.financials_over_time = {}
        for financial in self.__financials:
            current_period = financial['reportDate']
            self.financials_over_time[current_period] = CompanyFinancial(current_period, self.__cloud)

    def __init__(self, ticker, period, cloud):
        # period is 'quarter' or 'annual'
        # cloud is True or False
        # add these two to app/__init__.py
        self.__cloud = cloud

        if cloud == True:
            os.environ['IEX_API_VERSION'] = 'iexcloud-beta'
            os.environ['IEX_TOKEN'] = 'pk_172a73e7b4554b7ba9f06ebbad793dd3'
        else:
            os.environ['IEX_API_VERSION'] = 'v1'

        self.fetch_data(ticker, period)
        self.company_name = self.__key_stats['companyName']
        self.shares_outstanding = self.__key_stats['sharesOutstanding']
        self.market_cap = self.__key_stats['marketcap']
        self.market_price = self.market_cap / self.shares_outstanding
        self.dividends = [self.__dividends[i]['amount'] for i in range(len(divs))]

        for other_financial in self.__financials:
            current_period = other_financial['reportDate']
            if current_period not in self.financials_over_time.items():
                self.financials_over_time[current_period] = CompanyFinancial(current_period, self.__cloud)
            self.financials_over_time[current_period].add_other_financials(other_financial, self.shares_outstanding, self.market_price)

        if cloud == True:
            for cash_flow_statement in self.__cash_flow_statements:
                current_period = cash_flow_statement['reportDate']
                if current_period not in self.financials_over_time.items():
                    self.financials_over_time[current_period] = CompanyFinancial(current_period)
                self.financials_over_time[current_period].add_cash_flow_data(cash_flow_statement)

            for income_statement in self.__income_statements:
                current_period = income_statement['reportDate']
                if current_period not in self.financials_over_time.items():
                    self.financials_over_time[current_period] = CompanyFinancial(current_period)
                self.financials_over_time[current_period].add_income_data(income_statement)

        self.earnings_per_share = self.__key_stats['ttmEPS'] # directly from IEX
        self.pe_ratio_high = self.__key_stats['peRatioHigh']
        self.pe_ratio_low = self.__key_stats['peRatioLow']

    def to_dict(self):
        for key, value in self.financials_over_time.items():
            self.financials_over_time[key] = value.to_dict()

        to_return = {
            'peers': self.peers,
            'company_name': self.company_name,
            'shares_outstanding': self.shares_outstanding,
            'market_cap': self.market_cap,
            'market_price': self.market_price,
            'financials_over_time': self.financials_over_time,
            'earnings_per_share': self.earnings_per_share,
            'pe_ratio_high': self.pe_ratio_high,
            'pe_ratio_low': self.pe_ratio_low
        }
        return to_return

class CompanyFinancial:

    def __init__(self, period, cloud):
        self.period = period
        self.__cloud = cloud

    def add_cash_flow_data(self, cash_flow_statement):
        self.investing_cash_flow = cash_flow_statement['totalInvestingCashFlows']
        self.financing_cash_flow = cash_flow_statement['cashFlowFinancing']

    def add_income_data(self, income_statement):
        self.net_income = income_statement['netIncome']
        self.operating_income = income_statement['operatingIncome']

    def add_other_financials(self, other_financials, shares_outstanding, market_price):
        self.equity = other_financials['shareholderEquity']
        self.debt = other_financials['totalDebt']
        self.total_assets = other_financials['totalAssets']
        self.total_liabilities = other_financials['totalLiabilities'] # or should we get total liabilities
        self.debt_equity_ratio = self.total_liabilities / self.equity # online definition, you wrote it as debt/equity
        self.book_value = self.equity / shares_outstanding # your definition
        self.pbv_ratio = market_price / self.book_value
        self.risk = market_price - self.book_value
        self.margin_of_safety = self.equity / market_price
        self.current_ratio = self.total_assets / self.total_liabilities

    def to_dict(self):
        to_return = {
            'equity': self.equity,
            'debt': self.debt,
            'total_assets': self.total_assets,
            'total_liabilities': self.total_liabilities,
            'debt_equity_ratio': self.debt_equity_ratio,
            'book_value': self.book_value,
            'pbv_ratio': self.pbv_ratio,
            'risk': self.risk,
            'margin_of_safety': self.margin_of_safety,
            'current_ratio': self.current_ratio,
            'dividends': self.dividends
        }
        return to_return
