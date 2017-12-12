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
		

		if result > 0:
			error = 'User with this SSN already exists!'
			return render_template('html/register.html', error=error)

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
	flash('You are now logged out', 'success')
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
				session['userid'] = data['id']
				session['fname'] = data['fname']
				session['lname'] = data['lname']
				session['ssn'] = data['ssn']

				flash('You are now logged in', 'success')
				return redirect(url_for('transfer'))
			else:
				error = 'Invalid login!'
				curs.close()
				return render_template('html/login.html', error=error)
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

# Called in transfer to update the User's session savings balance.
def setSavingBalance(curs, amount):
	# Update transfering user account saving balance
	curs.execute("SELECT * FROM Accounts WHERE id = %s;", [session['accountID']])
	# Get new session value
	data = curs.fetchall()
	session['savingBalance'] = data[0]['savingBalance']
	total = (session['savingBalance'] - amount)

	return total

# Called in transfer to update the User's session checking balance.
def setCheckingBalance(curs, amount):
	# Update transfering user account saving balance
	curs.execute("SELECT * FROM Accounts WHERE id = %s;", [session['accountID']])
	# Get new session value
	data = curs.fetchall()
	session['checkingBalance'] = data[0]['checkingBalance']
	total = (session['checkingBalance'] - amount)

	return total


# Transfer funds to another account.
@app.route('/transfer', methods=['GET', 'POST'])
@is_logged_in
def transfer():

	if request.method == 'POST':

		accType = request.form.get('accountType')
		destAccType = request.form.get('destAccountType')

		amount = request.form['amount']	
		dest = request.form['destinationNum']


		# Convert string to int, assuming the value of amount is a string with numerical chars.
		amount = int(amount)
		# Needed to convert str to int, if never executed otherwise. 
		dest = int(dest)


		# Check for Negative amounts.
		if amount < 0:
			flash('Cannot transfer a negative amount!', 'danger')
			return render_template('html/transfer.html')

		# Check if trying to transfer to oneself.
		if dest == session['accountID'] and accType == destAccType:

			flash('Why are you transfering to yourself? Wasted CPU cycles!', 'danger')
			return render_template('html/transfer.html')


		curs = mysql.connection.cursor()

		results = curs.execute("SELECT * FROM Accounts where id = %s;", [dest])

		if results > 0:
			data = curs.fetchall()
			
		############ Refactor into function ##############

			destCheckBal = data[0]['checkingBalance']
			destSaveBal = data[0]['savingBalance']

			if accType == 'savingBalance':

				# print(type(destSaveBal), type(amount))
				if (session['savingBalance'] - amount) < 0:

					flash('You cannot overdraw from your SAVINGS account!', 'danger')
					return render_template('html/transfer.html')

				elif destAccType == 'savingBalance':
					# Update destination account saving balance first.
					print('saving 1')
					curs.execute("UPDATE Accounts SET savingBalance = %s WHERE id = %s;", (destSaveBal + amount, dest))


					total = setSavingBalance(curs, amount)
					curs.execute("UPDATE Accounts SET savingBalance = %s WHERE id = %s;", (total, session['accountID']))

					# Hope this works!
					mysql.connection.commit()


				else:
					print('checking 1')
					# Update destination account checking balance first.
					curs.execute("UPDATE Accounts SET checkingBalance = %s WHERE id = %s;", (destCheckBal + amount, dest))


					total = setSavingBalance(curs, amount)
					curs.execute("UPDATE Accounts SET savingBalance = %s WHERE id = %s;", (total, session['accountID']))

					# Hope this works!
					mysql.connection.commit()

			else: 
				# print(type(destSaveBal), type(amount))
				if (session['checkingBalance'] - amount) < 0:

					flash('You cannot overdraw from your CHECKING account!', 'danger')
					return render_template('html/transfer.html')

				elif destAccType == 'savingBalance':

					# Update destination account saving balance first.
					print('saving 2')
					curs.execute("UPDATE Accounts SET savingBalance = %s WHERE id = %s;", (destSaveBal + amount, dest))


					total = setCheckingBalance(curs, amount)
					# Update transfering user account saving balance
					curs.execute("UPDATE Accounts SET checkingBalance = %s WHERE id = %s;", (total, session['accountID']))

					# Hope this works!
					mysql.connection.commit()	
				else:

					print('checking 2')
					# Update destination account saving balance first.
					curs.execute("UPDATE Accounts SET checkingBalance = %s WHERE id = %s;", (destCheckBal + amount, dest))


					total = setCheckingBalance(curs, amount)
					curs.execute("UPDATE Accounts SET checkingBalance = %s WHERE id = %s;", (total, session['accountID']))

					# Hope this works!
					mysql.connection.commit()				


		##################################################


		else:
			error = 'That account number does not exist!'
			curs.close()
			return render_template('html/transfer.html', error=error)


		curs.close()

	return render_template('html/transfer.html')


@app.route('/logged_in')
@is_logged_in
def logged_in():
	flash("You logged in!", "success")
	return redirect(url_for('transfer'))

# If user has no account.
@app.route('/no_account', methods=['GET', 'POST'])
@is_logged_in
def no_account():

	form = AccountRegisterForm(request.form)
	if request.method == 'POST':
		pin = form.pin.data
		password = form.password.data

		# Encrypt the password BEFORE storing it into the database! 
		password = sha256_crypt.encrypt(str(form.password.data))

		# Create a connection to the DB.
		curs = mysql.connection.cursor()

		curs.execute("INSERT INTO Accounts (owner, password, pin) VALUES (%s, %s, %s);", (session['userid'], password, pin))

		mysql.connection.commit()
		curs.close()

		flash('You now have an account!', 'success')

		return redirect(url_for('account'))

	return render_template('html/no_account.html', form=form)

# Account 
@app.route('/account', methods=['GET', 'POST'])
@is_logged_in
def account():

	curs = mysql.connection.cursor()

	results = curs.execute("SELECT * FROM Accounts where owner = %s;", [session['userid']])

	if results > 0:


		data = curs.fetchall()

		session['accountLoaded'] = True
		session['savingBalance'] = data[0]['savingBalance']
		session['checkingBalance'] = data[0]['checkingBalance']
		session['accountID'] = data[0]['id']

		curs.close()
		return render_template('html/account.html', data=data)

	else:

		return redirect(url_for('no_account'))











