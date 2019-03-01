import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    
    # Disables feature of sql alchemy which notifies app every time change is about to be made
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = '823a9b472dd3067f787aad0670d861766169060b487edbbb'

	MONGODB_URI = os.environ.get('MONGODB_URI') or \
		'localhost:27017';

class ProductionConfig(Config):
	DEBUG=False

class StagingConfig(Config):
	DEVELOPMENT=True
	DEBUG=True

class DevelopmentConfig(Config):
	DEVELOPMENT=True
	DEBUG=True

class TestingConfig(Config):
	TESTING=True

