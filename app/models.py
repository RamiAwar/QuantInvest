import mongoengine
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
from app import login, app
from app import app
import redis
import rq
import pandas as pd
import datetime



class StockDailyPrice(mongoengine.Document):

    ticker = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True)
    price = mongoengine.FloatField(required=True)

    def to_dict(self):

        data = {
            'ticker': self.ticker,
            'date': self.date,
            'price': self.price
        }

        return data

    def get_tasks_in_progress(self):
        return Task.objects.get(job_id=self.ticker, complete=False)

    def get_task_in_progress(self, name):
        return Task.objects.get(name=name, job_id=self.ticker, complete=False).first()

    def __repr__(self):
        return '< Price of {} at {} >'.format(self.ticker, self.date)


class PortfolioDailyValue(mongoengine.EmbeddedDocument):

    date = mongoengine.DateTimeField(required=True)
    value = mongoengine.FloatField(required=True)

    def __repr__(self):
        return '< Portfolio Value on {} : {} >'.format(self.date, self.value)


class snp500_tickers(mongoengine.Document):

    symbol = mongoengine.StringField(required=True)
    name = mongoengine.StringField()
    sector = mongoengine.StringField()

    # Static function
    def initialize():
        if snp500_tickers.objects.first() != None:  # if the snp 500 tickers already exist in the database
            return
        snp_500_df = pd.read_csv('snp_500.csv')
        for index, row in snp_500_df.iterrows():
            s = snp500_tickers(symbol=row['Symbol'], name=row['Name'], sector=row['Sector'])
            s.save()

    def __repr__(self):
        return '< SnP500 : {} - object >'.format(self.symbol)


class Task(mongoengine.Document):

    job_id = mongoengine.StringField(required=True)
    complete = mongoengine.BooleanField(required=True, default=False)
    name = mongoengine.StringField(required=True)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100


class Allocation(mongoengine.EmbeddedDocument):

    ticker = mongoengine.StringField(required=True)
    weight = mongoengine.FloatField(required=True)

    def __repr__(self):
        return '<Allocation ' + self.ticker + ' : ' + self.weight + ' >'


class Portfolio(mongoengine.Document):

    user_id = mongoengine.ObjectIdField(required=True)
    timestamp = mongoengine.DateTimeField(required=True)

    expected_return = mongoengine.FloatField(required=True)
    volatility = mongoengine.FloatField(required=True)

    start_date = mongoengine.DateTimeField(required=True)
    end_date = mongoengine.DateTimeField(required=True)

    allocations = mongoengine.EmbeddedDocumentListField(Allocation, required=True)
    performance = mongoengine.EmbeddedDocumentListField(PortfolioDailyValue, required=True)

    sharpe_ratio = mongoengine.FloatField(required=True)

    profit = mongoengine.FloatField()


@login.user_loader
def load_user(id):
    user = None
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        # TODO: Log error : priority (3)
        pass

    return user


# Imports here to prevent circular import issue - will be refactored later.
from app.api.stock_fetcher.get_data import get_data, get_all_snp500_data
from app.api.backtest import backtest_portfolio

# TODO: separate auth models from others : priority (4)
class User(UserMixin, mongoengine.Document):

    username = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField(required=True)

    def __repr__(self):
        return '< User {} >'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # TODO: Change into something customizable?
    def get_profile_picture(self):
        return url_for('static', filename="example_user.png")

    def get_portfolios(self):

        portfolios = Portfolio.objects(user_id=self.pk);

        for portfolio in portfolios:

            # Perform extra backtest
            portfolio_dict = {x.ticker:(x.weight/100.0) for x in portfolio.allocations}


            stocks_df = get_data(list(portfolio_dict.keys()), portfolio.end_date,
                         datetime.datetime.now())

            backtest_results = backtest_portfolio(prices_df=stocks_df, portfolio=portfolio_dict,
                                                  initial_amount=portfolio.performance[0].value, window=50)

            labels = (list(backtest_results["total"].index))

            total_values = (list(backtest_results["total"].values))
            upper_values = (list(backtest_results["upper"].values))
            lower_values = (list(backtest_results["lower"].values))

            portfolio.profit = total_values[-1] - total_values[0]

        return portfolios;

