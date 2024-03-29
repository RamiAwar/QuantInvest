from flask import Flask
from flask_login import LoginManager

import mongoengine
from redis import Redis
import rq
import os
import pandas as pd

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

login = LoginManager(app)
login.login_view = "auth.login"  # For automatic redirects to and from login when protected pages are requested by anonymous users

from app import routes


# Register all blueprints
from app.errors import bp as errors_bp
from app.auth import bp as auth_bp
from app.profile_extractor import bp as extractor_bp
from app.api import bp as api_bp
from app.api.stock_fetcher import bp as stock_fetcher_bp
from app.api.backtest import bp as backtest_bp
from app.explorer import bp as explorer_bp

app.register_blueprint(errors_bp, url_prefix='/error')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(extractor_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(stock_fetcher_bp, url_prefix='/api/stock_fetcher')
app.register_blueprint(backtest_bp, url_prefix='/api/backtest')
app.register_blueprint(explorer_bp, url_prefix='/explorer')

# Assuming mongodb running on localhost 27017 (typical containerized version, port mapped 27017:27017)
mongoengine.connect(app.config['DB_NAME'], host=app.config['MONGODB_URI'], port=27017)

app.redis = Redis.from_url(app.config['REDIS_URL'])
app.snp500_data_queue = rq.Queue(app.config['CACHING_QUEUE'], connection=app.redis)


from app.models import *


@app.shell_context_processor
def make_shell_context():
    return {'User': User, 'StockDailyPrice': StockDailyPrice, 'snp500_tickers': snp500_tickers}


# TODO: Refactor into logger class (mail logger, nonmail logging) : priority (2)

# import logging
# from logging.handlers import SMTPHandler

# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)

# from logging.handlers import RotatingFileHandler
# import os

# # ...

# if not app.debug:
#     # ...

#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
#                                        backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)

#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Microblog startup')
