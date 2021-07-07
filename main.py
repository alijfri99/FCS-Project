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

from flask_ngrok import run_with_ngrok


@main.route('/')  # home page that return 'index'
def index():
    return render_template('index.html')


@main.route('/profile')  # profile page that return 'profile'
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/files')  # files page
def files():
    files_list = get_current_user_files(current_user.username)

    return render_template('files.html', name=current_user.name, files=files_list)


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
