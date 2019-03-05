from flask import render_template, flash, redirect, url_for, request, abort
from app import app
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
@login_required
def index():

	return render_template('index.html');


@app.route('/register', methods=['GET', 'POST'])
def register():

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	registration_form = RegistrationForm()

	if registration_form.validate_on_submit():

		user = User(username=registration_form.username.data, email=registration_form.email.data)
		user.set_password(registration_form.password.data)
		user.save()

		flash("User created successfully", category="success")
		return redirect(url_for('login'))

	return render_template('register.html', form=registration_form)



@app.route('/login', methods=['GET', 'POST'])
def login():


	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	login_form = LoginForm()
	
	# Validate fields on submission, if no errors continue
	if login_form.validate_on_submit():

		# Fetch user
		user = User.objects(email__exact=login_form.email.data).first()

		# Check username and password correctness
		if user is None or not user.check_password(login_form.password.data):

			flash("Invalid username or password", category="danger");
			return redirect(url_for('login'));

		# Login user
		login_user(user, remember=login_form.remember_me.data)
		
		# Redirect user to page tried to access while anonymous, or homepage if none
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '': # Make sure URL is relative not malicious
			next_page = url_for('index')
		
		return redirect(next_page)

	# If get request or form errors flashed, redirect to login
	return render_template('login.html', title="Login", form=login_form);


@app.route('/logout')
def logout():

	logout_user();
	return redirect(url_for('index'));


@app.route('/profile')
@login_required
def profile():

	user = current_user;
	
	# try:
	# 	user = User.objects.get(username=username)

	# except User.DoesNotExist:
	# 	abort(404);

	if user is not None:

		# Get profiles
		profiles = [
			{
				'name': 'Profile A',
				'exp_returns': 0.2,
				'exp_risk': 0.18
			},

			{
				'name': 'Profile B',
				'exp_returns': 0.24,
				'exp_risk': 0.34
			},

			{
				'name': 'Profile C',
				'exp_returns': 0.17,
				'exp_risk': 0.12
			},

			{
				'name': 'Profile D',
				'exp_returns': 0.12,
				'exp_risk': 0.1
			},

			{
				'name': 'Profile E',
				'exp_returns': 0.14,
				'exp_risk': 0.11
			}
			
		];

		return render_template('profile.html', user=user, profiles=profiles)

# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)






















