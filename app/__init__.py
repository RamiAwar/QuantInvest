from flask import Flask 
from flask_login import LoginManager

import mongoengine
import os


app = Flask(__name__);
app.config.from_object(os.environ['APP_SETTINGS'])

login = LoginManager(app);
login.login_view = "login" # For automatic redirects to and from login when protected pages are requested by anonymous users

# Workaround to circular imports! EW!
from app import routes

from app.models import User, Post


# Assuming mongodb running on localhost 27017 (typical containerized version, port mapped 27017:27017)
mongoengine.connect(app.config['DB_NAME'], host=app.config['MONGODB_URI'], port=27017);


# Make some variables available in flask shell
@app.shell_context_processor
def make_shell_context():
    return {'User': User, 'Post': Post}

