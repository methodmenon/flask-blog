#blog.py - controller

from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

#configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY= 'x04vvxe8x82x9d02rx86x12xe7x86xd0xd8woxe4x86x1dxe4tx90'

#create an instance of the Flask class
app = Flask(__name__)

#pulls in app configuration by looking at UPPERCASE variables
app.config.from_object(__name__)

#fucntion used for connecting to the db
def connect_db():
	return sqlite3.conect(app.config['DATABASE'])

@app.route('/', methods=['GET', 'POST'])
def login():
	#function compares the username and password entered agains those from the configuration section
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			#url_for() function generates an endpoint for the provided method --> so function is created for the main method
			return redirect(url_for('main'))
	return render_template('login.html', error=error)

@app.route('/main')
def main():
	return render_template('main.html')

if __name__ == '__main__':
	app.run(debug=True)

	