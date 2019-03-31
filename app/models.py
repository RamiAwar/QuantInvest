import mongoengine
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
from app import login, app
from app import app
import redis
import rq


# TODO: separate auth models from others : priority (4)
class User(UserMixin, mongoengine.Document):

    username = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField(required=True)

    def __repr__(self):
        return '< User {} >'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # TODO: Change into something customizable?
    def get_profile_picture(self):
        return url_for('static', filename="example_user.png")


class StockDailyPrice(mongoengine.Document):

	ticker = mongoengine.StringField(required=True)
	date = mongoengine.DateTimeField(required=True)
	price = mongoengine.FloatField(required=True)

	def to_dict(self):
		data = {
            'stock_ticker': self.stock_ticker,
            'date': self.date,
			'price': self.price
        }
		return data
	
	def get_tasks_in_progress(self):
		return Task.objects.get(job_id=self.stock_ticker, complete=False)

	def get_task_in_progress(self, name):
		return Task.objects.get(name=name, job_id=self.stock_ticker, complete=False).first()

	def __repr__(self):
		return '< Price of {} at {} >'.format(self.stock_ticker, self.date);
		

class Task(mongoengine.Document):
	job_id = mongoengine.StringField(required=True)
	complete = mongoengine.BooleanField(required=True, default=False)
	name = mongoengine.StringField(required=True)

	def get_rq_job(self):
		try:
			rq_job = rq.job.Job.fetch(self.id, connection=app.redis)
		except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
			return None
		return rq_job

	def get_progress(self):
		job = self.get_rq_job()
		return job.meta.get('progress', 0) if job is not None else 100

@login.user_loader
def load_user(id):
    user = None
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        # TODO: Log error : priority (3)
        pass

    return user
