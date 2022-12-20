from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.validity import email_check
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


# Req form, either GET or POST request
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Checks if already existing account, has right credentials for logging into it
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if it is POST req, it save the given credentials of the user
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password_one = request.form.get('password1')
        password_confirm = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')

        # Checks for validity
        if not email_check(email):
            flash('Email format is not valid.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password_one != password_confirm:
            flash('Passwords do NOT match.', category='error')
        elif len(password_one) < 5:
            flash('Password MUST be at least 7 characters', category='error')

        else:  # adding user to the database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password_one, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
