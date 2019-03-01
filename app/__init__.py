from flask import Flask 
from flask_login import LoginManager

import os


app = Flask(__name__);
app.config.from_object(os.environ['APP_SETTINGS'])

login = LoginManager(app);
login.login_view = "login" # For automatic redirects to and from login when protected pages are requested by anonymous users

# Workaround to circular imports! EW!
from app import routes

from app.models import User, Post


# Make some variables available in flask shell
@app.shell_context_processor
def make_shell_context():
    return {'User': User, 'Post': Post}

