from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.forms import EditProfileForm


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/')
@app.route('/landing')
def landing():

    if current_user.is_anonymous:
        return render_template('landing.html')
    else:
        return render_template('index.html')


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():

    edit_profile_form = EditProfileForm()

    if request.method == "POST":

        if edit_profile_form.validate_on_submit():

            current_user.username = edit_profile_form.username.data
            current_user.email = edit_profile_form.email.data
            current_user.save()

            flash('Your changes have been saved.')
            return redirect(url_for('profile'))

    return render_template('profile.html', user=current_user, form=edit_profile_form)


@app.route('/portfolios', methods=["GET"])
@login_required
def portfolios():
    
    return render_template('portfolios.html', user=current_user)


@app.route('/legal')
def legal():
    return render_template('legal.html')


@app.route('/about')
def about():
    return render_template('errors/under_construction.html')


@app.route('/blog')
def blog():
    return render_template('errors/under_construction.html')
