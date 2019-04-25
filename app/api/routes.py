from flask import jsonify, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from rq import Queue
from redis import from_url

from app import app
from app.api import bp
from app.models import Allocation, Portfolio, PortfolioDailyValue

import datetime


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
    job = None

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
    elif optimization_method == "target-return-volatility":
        job = queue.enqueue("app.api.optimizer.optimization_handlers.target_return_volatility", parameters)

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


@bp.route('/saveportfolio', methods=["POST"])
@login_required
def save_portfolio():

    parameters = request.get_json()

    # Create portfolio object from received parameters
    print("PARAMS")
    # print(parameters)

    if parameters["failed"]:
        flash("Invalid portfolio cannot be saved. Please try again.", category="danger")
        return render_template("portfolios.html", user=current_user)

    expected_return = parameters["data"]["statistics"]["expected_return"]
    volatility = parameters["data"]["statistics"]["volatility"]
    sharpe_ratio = parameters["data"]["statistics"]["sharpe_ratio"]

    print(expected_return)
    print(volatility)
    print(sharpe_ratio)

    weights_data = parameters["data"]["weights"]["data"]
    weights_tickers = parameters["data"]["weights"]["labels"]

    value_data_total = parameters["data"]["performance"]["total"]
    value_data_lower = parameters["data"]["performance"]["lower"]
    value_data_upper = parameters["data"]["performance"]["upper"]
    value_labels = parameters["data"]["performance"]["labels"]

    # Turn labels into datetime objects
    # September 18, 2017, 22:19:55 -> %B %d, %Y, %H:%M:%S
    # Mon, 21 March, 2015 -> %a, %d %B, %Y
    # Fri, 05 Oct 2018 00:00:00 GMT
    value_dates = [datetime.datetime.strptime(label, "%a, %d %b %Y %H:%M:%S %Z") for label in value_labels]

    portfolio_daily_values = [PortfolioDailyValue(date=date, value=value)
                              for (date, value) in zip(value_dates, value_data_total)]

    allocations = [Allocation(ticker=ticker, weight=weight) for (ticker, weight) in zip(weights_tickers, weights_data)]

    # print(portfolio_daily_values)

    start_date = value_dates[0]
    end_date = value_dates[-1]

    portfolio = Portfolio(user_id=current_user.get_id(),
                          timestamp=datetime.datetime.now(),
                          expected_return=expected_return,
                          volatility=volatility,
                          start_date=start_date,
                          end_date=end_date,
                          allocations=allocations,
                          performance=portfolio_daily_values,
                          sharpe_ratio=sharpe_ratio
                          )
    portfolio.save()

    return jsonify(True)
