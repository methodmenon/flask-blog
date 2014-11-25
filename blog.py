#blog.py - controller

from flask import Flask, render_template, request, session, \
	flash, redirect, url_for, g
import sqlite3

#configuration
DATABASE = 'blog.db'

#create an instance of the Flask class
app = Flask(__name__)

#pulls in app configuration by looking at UPPERCASE variables
app.config.from_object(__name__)

#fucntion used for connecting to the db
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
	app.run(debug=True)

	