#!/usr/bin/env python3

import os
import pymysql as ps
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

def connect_db():
	"""Connects to the specific database."""
	engine = create_engine(app.config['DATABASE'])


	# return rv

connect_db()