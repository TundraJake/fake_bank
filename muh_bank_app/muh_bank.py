'''
Jacob McKenna 
UAF CS492 Computer Security I 
muh_bank.py file
	Has app configurations to run bank web application.
'''
import os
import pymysql.cursors

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from .templates.forms.register import *

from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
	# DATABASE='mysql://banker:banking@localhost/MuhBank',
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

app.config.from_envvar('MUHBANK_SETTINGS', silent=True)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'banker'
app.config['MYSQL_PASSWORD'] = 'banking'
app.config['MYSQL_DB'] = 'MuhBank'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)






# Home page 
@app.route('/')
def home():
	return render_template('html/home.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

	form = UserRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		firstName = form.firstName.data 
		lastName = form.lastName.data
		email = form.email.data
		ssn = form.ssn.data

		# Encrypt the password BEFORE storing it into the database! 
		password = sha256_crypt.encrypt(str(form.password.data))

		# Create a connection to the DB.
		curs = mysql.connection.cursor()

		result = curs.execute("SELECT * FROM User WHERE ssn = %s;", [ssn])
		print(result)

		if result > 0:
			error = "User with this SSN already exists!"
			return render_template('html/register.html')
		else:

			curs.execute("INSERT INTO User (fname, lname, email, ssn, password) VALUES (%s, %s, %s, %s, %s);", (firstName, lastName, email, ssn, password))

			# Commit changes to DB.
			mysql.connection.commit()

			# Close connection! 
			curs.close()

			flash('You are now registered', 'success')
			
			return redirect('login')


	return render_template('html/register.html', form=form)


# Logout 
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))




# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':

		email = request.form['email']
		passwordCandidate = request.form['password']

		curs = mysql.connection.cursor()

		result = curs.execute("SELECT * FROM User where email = %s;", [email])

		if result > 0:
			data = curs.fetchone()
			password = data['password']

			# Hash the password candidate and compare.
			if sha256_crypt.verify(passwordCandidate, password):
				session['logged_in'] = True
				session['firstName'] = data['fname']

				print('do I get here 3')
				flash('You are now logged in', 'success')
				return redirect(url_for('transfer'))
			else:
				error = 'Invalid login!'
				curs.close()
				return render_template('html/login.html')
		else:
			error = 'Username not found'
			return render_template('html/login.html', error=error)

	return render_template('html/login.html')


# Check if the user is logged in. 
# Need this to 
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

# Logged in 
@app.route('/transfer')
@is_logged_in
def transfer():
	return render_template('html/transfer.html')


@app.route('/logged_in')
@is_logged_in
def logged_in():
	flash("You logged in!", "success")
	return redirect(url_for('transfer'))










