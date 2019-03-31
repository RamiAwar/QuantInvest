from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from rq import Queue
from redis import from_url 

from app import app
from app.api import bp


@bp.route('/simpleopt', methods=["POST"])
@login_required
def optimize_simple():

	# Get parameters as dictionary
	parameters = request.get_json();

	# Create job in optimization queue
	queue = Queue(app.config["OPTIMIZER_QUEUE"], connection=from_url(app.config["REDIS_URL"]))
	job = queue.enqueue("app.api.optimizer.optimization_handlers.efficient_risk_volatility", parameters)

	
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

	result["is_finished"] = job.is_finished;
	result["is_failed"] = job.is_failed;
	result["result"] = job.result;


	return jsonify(result);



