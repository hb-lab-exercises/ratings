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

    if User.query.filter(User.email == email).first():
        # If email exists (i.e. is duplicate) 
        flash("Email already exists!")
        return redirect('/register')

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

    email = request.form.get("email")
    password = request.form.get("password")

    # query for that email address in database (returns Truthly/Falsey (none))   
    user_id = db.session.query(User.user_id).filter(User.email==email,
                                       User.password==password).first()
    # Check if email matches the password 
    if user_id:
        #log user in - adding user id - from db to flask session
        flash("Logged in")
        session["User"] = user_id
        return redirect("/")
    else:
        flash("Error: Username/Password is invalid")
        return redirect("/")


@app.route('/logout')
def logout_process():
    """Logs out user"""

    # removes user id from session
    del session["User"]
    flash("Logged Out")
    
    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<user_id>')
def user_details(user_id):
    """Show details about a user."""

    user_object = db.session.query(User).filter(User.user_id==user_id).first()

    return render_template('user_details.html', 
                            user_object=user_object)


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
