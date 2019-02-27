import mongoengine

# Assuming mongodb running on localhost 27017 (typical containerized version, port mapped 27017:27017)
mongoengine.connect('flask_mega');



class User(mongoengine.Document):

    _id = mongoengine.ObjectIdField()
    username = mongoengine.StringField()
    email = mongoengine.StringField()
    password_hash = mongoengine.StringField()

    def __repr__(self):
        return '< User {} >'.format(self.username) 

class Post(mongoengine.Document):

	_id = mongoengine.ObjectIdField()
	body = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField()
	user_id = mongoengine.ObjectIdField()

	def __repr__(self):
		return '< Post by {} at {} >'.format(self.user_id, self.timestamp);