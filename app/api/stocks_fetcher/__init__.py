from flask import Blueprint
import pandas as pd

bp = Blueprint('data_fetching', __name__)

snp_500_df = pd.read_csv('snp_500.csv')

from app.stock_prices import routes