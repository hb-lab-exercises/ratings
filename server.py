"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_form():
    """Displays registration form"""

    return render_template("registration_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Processes registration form"""

    # Grab data from form
    email = request.form.get('email')
    password = request.form.get('password')


    if  User.query.filter(User.email == email).first().email:
       # User.query(User.email).filter(User.email == email).first() 
       flash("Email already exists!")
       return redirect('/register')
    else:
        # Adds and commits user's email and password into the database 
        db.session.add(User(email=email, password=password))
        db.session.commit()
        return redirect('/')

@app.route('/login', methods=["GET"])
def login_form():
    """Displays login form"""

    return render_template("login_form.html")


@app.route('/login', methods =["POST"])
def login_process():
    """Redirects user to homepage after login message"""


    # query for that email address in database
        # if email matches the password 
            #log user in - adding user id - from db to flask session
            # flash("Logged in")
            # redirect back to homepage
        # else error message 
            # redirect back to login page?
            # hyperlink registration page
    return redirect("/")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
