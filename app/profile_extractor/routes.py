from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required


from app import app
from app.models import User
from app.profile_extractor import bp

@bp.route('/extractprofile', methods=["GET"])
@login_required
def extractprofile():
    return render_template('risk_assessment_questionnaire.html')


@bp.route('/createprofile', methods=['GET'])
@login_required
def createprofile():

	# registration_form = RegistrationForm()

	# if registration_form.validate_on_submit():

	# 	user = User(username=registration_form.username.data, email=registration_form.email.data)
	# 	user.set_password(registration_form.password.data)
	# 	user.save()

	# 	flash("User created successfully", category="success")
	# 	return redirect(url_for('auth.login'))



	return render_template('profile_extractor/profile_extractor.html', basic=False)

# @bp.route('/')



