'''
Jacob McKenna 
UAF CS492 Computer Security I 
muh_bank.py file
	Has app configurations to run bank web application.
'''
import os
import pymysql.cursors

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

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


# Create a connection to database.
connection = pymysql.connect(host='localhost', 
							port=3306, 
							user='banker', 
							passwd='banking', 
							db='MuhBank',
							unix_socket="/tmp/mysql.sock")

def connect_db():
	"""Connects to the specific database."""
	
	cursor = connection.cursor()
	print('Cant do this anymore')

	# return rv

connect_db()

###############################################
###############################################
###############################################
# Project views
@app.route('/')
def show_entries():
    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # entries = cur.fetchall()
    return render_template('html/show_entries.html', entries=entries)

@app.route('/logged_in')
def loggedIn():
	return 'You\'re logged in!'

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

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
            return redirect(url_for('/logged_in'))
    return render_template('html/login.html', error=error)











