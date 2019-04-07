from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from rq import Queue
from redis import from_url

from app import app
from app.api import bp



@bp.route('/optimize', methods=["POST"])
@login_required
def optimize():
    """Optimization endpoint that handles all optimization methods and creates corresponding jobs.

    Expected json request data:
    {
        "ticker_list": ticker_list,
        "start_date": start_date,
        "end_date": end_date,
        "optimization_method": optimization_method,
        "optimization_parameters": {
            "target_volatility": 0.12,
            "target_return": 0.2
        }
    }

    Decorators:
        bp.route
        login_required

    Returns:
        JSON Object -- job_id
    """

    # Get parameters as dictionary
    parameters = request.get_json()

    # Create queue object
    queue = Queue(app.config["OPTIMIZER_QUEUE"], connection=from_url(app.config["REDIS_URL"]))

    # Check type of optimization
    optimization_method = parameters["optimization_method"]

    if optimization_method == "max-sharpe":
        job = queue.enqueue("app.api.optimizer.optimization_handlers.max_sharpe", parameters)
    elif optimization_method == "min-volatility":
        job = queue.enqueue("app.api.optimizer.optimization_handlers.min_volatility", parameters)
    elif optimization_method == "min-volatility-target":
        job = queue.enqueue("app.api.optimizer.optimization_handlers.min_volatility_target", parameters)
    elif optimization_method == "max-return-target":
        job = queue.enqueue("app.api.optimizer.optimization_handlers.max_return_target", parameters)

    return jsonify({"job_id": job._id})


@bp.route('/checkstatus', methods=["POST"])
@login_required
def check_job_status():

    parameters = request.get_json()
    job_id = parameters["job_id"]

    # Check job status
    queue = Queue(app.config["OPTIMIZER_QUEUE"], connection=from_url(app.config["REDIS_URL"]))
    job = queue.fetch_job(job_id)

    print("CHECK STATUS   :  ", job)

    result = {}

    result["is_finished"] = job.is_finished
    result["is_failed"] = job.is_failed
    result["result"] = job.result

    # print(job.result);
    return jsonify(result)
