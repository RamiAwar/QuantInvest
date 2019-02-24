from flask import Flask 

app = Flask(__name__);

# Workaround to circular imports! EW!
from app import routes



