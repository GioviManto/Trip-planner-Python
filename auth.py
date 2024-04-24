# Import necessary modules and components from the Flask framework
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User  # Import the User model from the website module
from werkzeug.security import generate_password_hash, check_password_hash  # Import functions for password hashing
from website import user_db  # Import the user database object
from flask_login import login_user, login_required, logout_user, current_user  # Import components for user authentication

# Create a Blueprint named 'auth'
auth = Blueprint('auth', __name__)

# Route for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the request method is either GET or POST
    if request.method == 'POST' or 'GET':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('firstName')

        # Print user input for debugging purposes
        print(email)
        print(password)
        print(name)

        # Query the database for the user with the provided email
        user = User.query.filter_by(email=email).first()
        print('User: ', user)
        if user:
            # If the user exists, check the provided password
            if request.method == 'POST':
                if check_password_hash(user.password, password):
                    # If the password is correct, log in the user
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

    # Render the login template with the current user and username
    return render_template("login.html", user=current_user, username=name)

# Route for user logout (requires user to be logged in)
@auth.route('/logout')
@login_required
def logout():
    # Log the user out and redirect to the login page
    flash('Logged out successfully', category='success')
    logout_user()
    return redirect(url_for('auth.login'))

# Route for user registration
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Check if the request method is POST
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Query the database for an existing user with the provided email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user and add it to the database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            user_db.session.add(new_user)
            user_db.session.commit()
            # Log in the new user and redirect to the home page
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    # Render the sign-up template with the current user
    return render_template("sign_up.html", user=current_user)

# Route for the home page (requires user to be logged in)
@auth.route('/home')
@login_required
def home():
    # Print information about the current user for debugging purposes
    print('User in home: ', current_user)
    username = current_user.first_name
    print('Username in home: ', username)
    # Render the home template with the current user and username
    return render_template("home.html", user=current_user, username=username)
