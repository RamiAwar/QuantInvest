from flask import Blueprint

bp = Blueprint('fundamentals_fetcher', __name__)

from app.api.stock_fetcher import get_fundamentals