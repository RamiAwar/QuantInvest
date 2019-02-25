from flask import Flask 
import os

app = Flask(__name__);
app.config.from_object(os.environ['APP_SETTINGS'])



# Workaround to circular imports! EW!
from app import routes




