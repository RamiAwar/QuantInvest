from flask import Blueprint
import pandas as pd

bp = Blueprint('data_fetching', __name__)

from app.api.stock_prices import routes