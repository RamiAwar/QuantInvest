from flask import Blueprint

bp = Blueprint('backtest', __name__)

from app.api.backtest import routes