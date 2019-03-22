from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from rq import Queue
from worker import conn

from app import app
from app.api import bp


@bp.route('/optimize')
@login_required
def optimize_portfolio():

	# Get parameters
	parameters = request.args;

	# Create worker thread
	conn = redis.from_url(redis_url)
	q = Queue(connection=conn)

	job_id = q.enqueue(count_words_at_url, app.config.REDIS_URL)


