from flask import render_template
from app import app
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user

@app.route('/')
@app.route('/index')
def index():

	user = {'username': 'Test'}

	return render_template('index.html', title="Home", user=user);



@app.route('/login', methods=['GET', 'POST'])
def login():


	# TODO: Hide case by hiding Login redirection buttons for authenticated users : priority (1)
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	login_form = LoginForm()
	if login_form.validate_on_submit():

		# Fetch user
		user = User.objects(username__exact=login_form.username.data).first()

		# Check username and password correctness
		if user is None or not user.check_password(form.password.data):

			flash("Invalid username or password");
			return redirect(url_for('login'));

		login_user(user, remember=login_form.remember_me.data)
		return redirect(url_for('index'))


	return render_template('login.html', title="Login", form=login_form);


@app.route('/logout')
def logout():

	logout_user();
	return redirect(url_for('index'));























