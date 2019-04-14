from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required


from app import app
from app.models import User
from app.profile_extractor import bp

@bp.route('/extractprofile', methods=["GET"])
@login_required
def extractprofile():
    return render_template('risk_assessment_questionnaire.html')


@bp.route('/createprofile', methods=['GET', "POST"])
@login_required
def createprofile():

	# registration_form = RegistrationForm()

	# if registration_form.validate_on_submit():

	# 	user = User(username=registration_form.username.data, email=registration_form.email.data)
	# 	user.set_password(registration_form.password.data)
	# 	user.save()

	# 	flash("User created successfully", category="success")
	# 	return redirect(url_for('auth.login'))
 
    basic = False;
    expected_return = 0;
    expected_volatility = 0;

    if request.method == "POST":

        # Received request from risk assesser
        basic = True

        # TODO: Convert risk score to expected return, expected volatility
        

        # TODO: Render template with basic optimization page active, with expected return and volatility 


    return render_template('profile_extractor/profile_extractor.html', basic=basic, expected_return=expected_return, expected_volatility=expected_volatility)

# @bp.route('/')



