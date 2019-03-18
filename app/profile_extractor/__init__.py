from flask import Blueprint

bp = Blueprint('profile_extractor', __name__)

from app.profile_extractor import routes