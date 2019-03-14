import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = '823a9b472dd3067f787aad0670d861766169060b487edbbb'

	MONGODB_URI = os.environ.get('MONGODB_URI') or \
		'localhost:27017';
	DB_NAME = 'quantinvest'

class ProductionConfig(Config):
	DEBUG=False

class StagingConfig(Config):
	DEVELOPMENT=True
	DEBUG=True

class DevelopmentConfig(Config):
	DEVELOPMENT=True
	DEBUG=True
	DB_NAME = 'flask_mega'

class TestingConfig(Config):
	TESTING=True

