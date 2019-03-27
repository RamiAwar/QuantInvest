from flask import Blueprint

bp = Blueprint('backtest', __name__)

from app.backtest import routes