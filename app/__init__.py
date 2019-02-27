from flask import Flask 
import os

app = Flask(__name__);
app.config.from_object(os.environ['APP_SETTINGS'])


# Workaround to circular imports! EW!
from app import routes

from app.models import User, Post


# Make some variables available in flask shell
@app.shell_context_processor
def make_shell_context():
    return {'User': User, 'Post': Post}


print(User.objects())


print(User.objects(email__contains='rami'))

