from flask import render_template
from app import app
from app.forms import LoginForm

from flask_login import current_user, login_user

@app.route('/')
@app.route('/index')
def index():

	user = {'username': 'Test'}

	return render_template('index.html', title="Home", user=user);



@app.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	login_form = LoginForm()

	if login_form.validate_on_submit():
        
		flash('Login requested for user with email {}, remember_me={}'.format(login_form.email.data, login_form.remember_me.data))
		return redirect(url_for('index'))

	return render_template('login.html', title="Login", form=login_form);

























