from flask import Flask 
import os

app = Flask(__name__);
app.config.from_object(os.environ['APP_SETTINGS'])

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Workaround to circular imports! EW!
from app import routes, models




