'''
Jacob McKenna 
UAF CS492 Computer Security I 
muh_bank.py file
	Has app configurations to run bank web application.
'''
import os
import pymysql.cursors

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_bootstrap import Bootstrap

from flask_mysqldb import MySQL

from .templates.forms.register import *

from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

from passlib.hash import sha256_crypt

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
	DATABASE='mysql://banker:banking@localhost/MuhBank',
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

app.config.from_envvar('MUHBANK_SETTINGS', silent=True)







# Project views
@app.route('/')
def home():

	return render_template('html/home.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data 
		email = form.email.data
		username = form.username.data

		# Encrypt the password BEFORE storing it into the database! 
		password = sha256_crypt.encrypt(str(form.password.data))


	return render_template('html/register.html', form=form)





@app.route('/logout')
def logout():
	session.clear()
	flash('You were logged out')
	return redirect(url_for('home'))

	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('logged_in'))
	return render_template('html/login.html', error=error)



# Logged in 
@app.route('/transfer')
def transfer():

	return render_template('html/transfer.html')


@app.route('/logged_in')
def logged_in():
	flash("You logged in!", "success")
	return redirect(url_for('transfer'))










