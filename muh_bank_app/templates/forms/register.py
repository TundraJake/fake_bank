from wtforms import Form, BooleanField, TextField, HiddenField, PasswordField,\
DateTimeField, validators, IntegerField, SubmitField, SelectField, StringField

from flask_wtf import FlaskForm

# User registration. 
class RegisterForm(Form):

    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=10, max=50),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
