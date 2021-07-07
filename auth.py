########################################################################################
######################          Import packages      ###################################
########################################################################################
import subprocess

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import User, SysAudit
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
from datetime import datetime

auth = Blueprint('auth', __name__)  # create a Blueprint object that we name 'auth'


@auth.route('/login', methods=['GET', 'POST'])  # define login page path
def login():  # define login page function
    if request.method == 'GET':  # if the request is a GET we return the login page
        return render_template('login.html')

    else:  # if the request is POST the we check if the user exist and with te right password
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(username=username).first()
        try:
            new_audit = SysAudit(username=username, password=password, ip_address=request.headers['x-forwarded-for'],
                                 user_agent=request.headers['user-agent'], date_and_time=datetime.now())
        except KeyError:
            new_audit = SysAudit(username=username, password=password, ip_address=request.remote_addr,
                                 user_agent=request.headers.get('User-Agent'), date_and_time=datetime.now())
        # add the new user to the database
        db.session.add(new_audit)
        db.session.commit()

        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Your username is not in database!')
            return redirect(url_for('auth.login'))
        elif not check_password_hash(username, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))


def check_password_hash(username, passwd):
    try:
        ps = subprocess.Popen(('cat', '/etc/shadow'), stdout=subprocess.PIPE)
        output = subprocess.check_output(('grep', username), stdin=ps.stdout)
        ps.wait()
    except subprocess.CalledProcessError:
        print(f"Error: grep empty for : {username} {passwd}")
        return False

    if len(output) < 1:
        return False

    hash_elements = output.decode("utf-8").split("$")
    hashing_algorithm_number = hash_elements[1]
    salt = hash_elements[2]
    hash_str1 = hash_elements[3].split(":")[0].strip()

    output = subprocess.check_output(["openssl", "passwd", f"-{hashing_algorithm_number}", "-salt", salt, passwd])
    hash_elements = output.decode("utf-8").split("$")
    hash_str2 = hash_elements[3].strip()
    print(f"hash_str1 : {hash_str1}, hash_str2 : {hash_str2}")
    return hash_str1 == hash_str2


@auth.route('/logout')  # define logout path
@login_required
def logout():  # define the logout function
    logout_user()
    return redirect(url_for('main.index'))
