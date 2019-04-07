from flask import Blueprint
import pandas as pd

bp = Blueprint('stock_fetcher', __name__)

from app.api.stock_fetcher import routes