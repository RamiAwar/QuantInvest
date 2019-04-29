from flask import Blueprint

bp = Blueprint('explorer', __name__)

from app.explorer import routes