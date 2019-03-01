from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, login_required

@app.route('/')
@app.route('/index')
@login_required
def index():

	user = {'username': 'Test'}

	return render_template('index.html', title="Home", user=user);



@app.route('/login', methods=['GET', 'POST'])
def login():


	# TODO: Hide case by hiding Login redirection buttons for authenticated users : priority (1)
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
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		
		return redirect(next_page)

	# If get request or form errors flashed, redirect to login
	return render_template('login.html', title="Login", form=login_form);


@app.route('/logout')
def logout():

	logout_user();
	return redirect(url_for('index'));























