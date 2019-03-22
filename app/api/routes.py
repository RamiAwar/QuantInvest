from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from rq import Queue
from redis import from_url 

from app import app
from app.api import bp


# TODO: Remove temporary import : priority (1)
import time 

# from app.api.cors import crossdomain

def do_nothing():

	for i in range(5):
		print(i)
		time.sleep(1);


	print("END");


@bp.route('/optimize', methods=["POST"])
@login_required
def optimize_portfolio():

	# Get parameters as dictionary
	parameters = request.get_json();

	# Create worker thread
	queue = Queue(app.config["OPTIMIZER_QUEUE"], connection=from_url(app.config["REDIS_URL"]))

	job = queue.enqueue("app.api.optimizer.optimization_handlers.optimize", parameters)
	
	return jsonify({"job_id": job._id })


@bp.route('/checkstatus', methods=["POST"])
@login_required
def check_job_status():

	parameters = request.get_json();
	job_id = parameters["job_id"];



	# Check job status
	queue = Queue(app.config["OPTIMIZER_QUEUE"], connection=from_url(app.config["REDIS_URL"]))
	job = queue.fetch_job(job_id)

	print("CHECK STATUS   :  ", job)

	result = {}

	if job.is_finished:

		print(job.result);
		result["is_finished"] = True;
		result["result"] = job.result

	else:

		result["is_finished"] = False;


	return jsonify(result);



