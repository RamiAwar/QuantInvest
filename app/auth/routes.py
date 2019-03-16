from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.auth import bp



@bp.route('/register', methods=['GET', 'POST'])
def register():

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	registration_form = RegistrationForm()

	if registration_form.validate_on_submit():

		user = User(username=registration_form.username.data, email=registration_form.email.data)
		user.set_password(registration_form.password.data)
		user.save()

		flash("User created successfully", category="success")
		return redirect(url_for('auth.login'))

	return render_template('auth/register.html', form=registration_form)



@bp.route('/login', methods=['GET', 'POST'])
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
			return redirect(url_for('auth.login'));

		# Login user
		login_user(user, remember=login_form.remember_me.data)
		
		# Redirect user to page tried to access while anonymous, or homepage if none
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '': # Make sure URL is relative not malicious
			next_page = url_for('index')
		
		return redirect(next_page)

	# If get request or form errors flashed, redirect to login
	return render_template('auth/login.html', title="Login", form=login_form);


@bp.route('/logout')
def logout():

	logout_user();
	return redirect(url_for('index'));
