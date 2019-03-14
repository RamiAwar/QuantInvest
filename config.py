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

	# TODO: Correct setup : priority (2)
	# MAIL_SERVER = os.environ.get('MAIL_SERVER')
 #    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
 #    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
 #    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
 #    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
 #    ADMINS = ['your-email@example.com']

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

