#blog.py - controller

from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

#configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'x04vvxe8x82x9d02rx86x12xe7x86xd0xd8woxe4x86x1dxe4tx90'

#create an instance of the Flask class
app = Flask(__name__)

#pulls in app configuration by looking at UPPERCASE variables
app.config.from_object(__name__)

#fucntion used for connecting to the db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#decorator to check if user is logged in in order to access main.html
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into posts (title, post) values (?,?)', [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted')
        return redirect(url_for('main'))



if __name__ == '__main__':
    app.run(debug=True)

