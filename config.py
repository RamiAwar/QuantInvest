import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = '823a9b472dd3067f787aad0670d861766169060b487edbbb'

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

