import mongoengine
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login, app


# Assuming mongodb running on localhost 27017 (typical containerized version, port mapped 27017:27017)
mongoengine.connect('flask_mega', host=app.config['MONGODB_URI'], port=27017);



class User(UserMixin, mongoengine.Document):

    _id = mongoengine.ObjectIdField()
    username = mongoengine.StringField()
    email = mongoengine.StringField()
    password_hash = mongoengine.StringField()

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password);

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password);


    def __repr__(self):
        return '< User {} >'.format(self.username) 

class Post(mongoengine.Document):

	_id = mongoengine.ObjectIdField()
	body = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField()
	user_id = mongoengine.ObjectIdField()

	def __repr__(self):
		return '< Post by {} at {} >'.format(self.user_id, self.timestamp);


@login.user_loader
def load_user(_id):
	return User.objects.get(id=_id);












