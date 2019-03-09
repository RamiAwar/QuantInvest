from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo

from app.models import User

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Sign Up")


	# Adding custom validators on top of stock validators
	# validate_<field_name>

	def validate_username(self, username):

		user = None;

		try:
			user = User.objects.get(username=username.data);

		except User.DoesNotExist:
			return

		if user is not None:
			raise ValidationError("Username already taken. Please choose another.")

	def validate_email(self, email):

		user = None;
		try:
			user = User.objects.get(email=email.data);
		except User.DoesNotExist:
			return
			
		if user is not None:
			raise ValidationError("Email associated to an existing account. Please choose another.")

	def validate_password(self, password):

		if len(password.data) < 8:
			raise ValidationError("Password needs to be at least 8 characters long.");

		# TODO: Add more safety checks : priority (7)

class EditProfileForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])

	submit = SubmitField('Update Profile')









