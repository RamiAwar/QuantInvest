from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from rq import Queue
from redis import from_url 

from app import app
from app.api import bp

# from app.api.cors import crossdomain

def do_nothing():
	pass;

@bp.route('/optimize', methods=["POST"])
@login_required
def optimize_portfolio():

	# Get parameters as dictionary
	parameters = request.get_json();

	# Create worker thread
	queue = Queue(app.config["OPTIMIZER_QUEUE"], connection=from_url(app.config["REDIS_URL"]))

	job_id = queue.enqueue("app.api.optimizer.optimization_handlers.optimize", parameters)
	
	return jsonify({"name":"TZEST"})

