########################################################################################
######################          Import packages      ###################################
########################################################################################
import subprocess

from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app, db

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)


@main.route('/')  # home page that return 'index'
def index():
    return render_template('index.html')


@main.route('/profile')  # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/files')  # files page
@login_required
def files():
    files_list = get_current_user_files(current_user.username)

    return render_template('files.html', name=current_user.name, files=files_list)


def get_top_passwords():
    query = """SELECT password, count(password) 
  FROM sys_audit 
 GROUP by password ORDER BY count(password) DESC limit 10;"""
    return db.engine.execute(query)


def get_top_usernames():
    query = """SELECT username, count(username) 
  FROM sys_audit 
 GROUP BY username ORDER BY count(username) DESC limit 10;"""
    return db.engine.execute(query)


def get_top_userpasswords():
    query = """SELECT username, password, count(*)
FROM sys_audit
GROUP BY username, password ORDER BY count(*) DESC limit 10;"""
    return db.engine.execute(query)


@main.route('/stats')  # stats page
@login_required
def stats():
    return render_template('stats.html', top_usernames=get_top_usernames(), top_passwords=get_top_passwords(),
                           top_userpasswords=get_top_userpasswords())


def get_current_user_files(username):
    output = subprocess.check_output(f"cd files && find -exec sudo -u {username} test -r '{{}}' \; -print",
                                     shell=True).decode("utf-8")

    return output.splitlines()[1:]


app = create_app()  # we initialize our flask app using the __init__.py function
# app = Flask(__name__)
# run_with_ngrok(app)  # Start ngrok when app is run

if __name__ == '__main__':
    db.create_all(app=create_app())  # create the SQLite database
    app.run(debug=True, host='0.0.0.0', port=5000)  # run the flask app on debug mode
    # app.run()  # run the flask app on debug mode
