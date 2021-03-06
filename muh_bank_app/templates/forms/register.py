'''
Jacob McKenna 
UAF CS492 Computer Security I 
	register.py - Stores the forms for register Users and Accounts.
'''
from wtforms import Form, BooleanField, TextField, HiddenField, PasswordField,\
DateTimeField, validators, IntegerField, SubmitField, SelectField, StringField

from flask_wtf import FlaskForm

# User registration. 
class UserRegisterForm(Form):

	firstName = StringField('First Name', [validators.Length(min=1, max=50)])
	lastName = StringField('Last Name', [validators.Length(min=1, max=50)])
	email = StringField('Email', [validators.Length(min=10)])
	ssn = StringField('Social Security Number', [validators.Length(min=9, max=9)])

	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.Length(min=10, max=40),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

# Account registration
class AccountRegisterForm(Form):
	pin = IntegerField('Pin',  [validators.Length(min=4,max=6)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.Length(min=10, max=40),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')
