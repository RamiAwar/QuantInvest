import mongoengine
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
from app import login, app


# TODO: separate auth models from others : priority (1)
class User(UserMixin, mongoengine.Document):

    username = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField(required=True)

    def __repr__(self):
        return '< User {} >'.format(self.username) 

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password);

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password);

    # TODO: Change into something customizable?
    def get_profile_picture(self):
    	return url_for('static', filename="example_user.png")

    
class Post(mongoengine.Document):

	body = mongoengine.StringField(required=True)
	timestamp = mongoengine.DateTimeField(required=True)
	user_id = mongoengine.ObjectIdField(required=True)

	def __repr__(self):
		return '< Post by {} at {} >'.format(self.user_id, self.timestamp);

class StockDailyPrice(mongoengine.Document):
	stock_ticker = mongoengine.StringField(required=True)
	date = mongoengine.DateTimeField(required=True)
	open_price = mongoengine.FloatField(required=True)
	def __repr__(self):
		return '< Price of {} at {} >'.format(self.stock_ticker, self.date);

@login.user_loader
def load_user(id):
	user = None;
	try:
		user = User.objects.get(pk=id);
	except User.DoesNotExist:
		# TODO: Log error : priority (3)
		pass

	return user;













