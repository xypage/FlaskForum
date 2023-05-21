import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskforum.db import get_db

bp = Blueprint('login', __name__, url_prefix='/login')


# Creates a new user, this is /login/new
@bp.route('/new', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        display_name = request.form['display_name']
        password = request.form['password']
        db = get_db()
        error = None

        # Check for required fields
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        # If a display name wasn't provided, default it to their username
        if not display_name:
            display_name = username

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, display_name) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), display_name),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("login.login"))

        flash(error)

    return render_template('login/register.html')


# Logs into existing user, at /login
@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login/login.html')

# Lets us access the logged in user during any request at g.user 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# Clears the user_id from the session, effectively logging out the user,
# then sends them back to home
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Gives us a decorator that we'll be able to use for our other views that makes sure _someone_ is logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # And specifically, if they're not logged in, send them to the login page
        if g.user is None:
            return redirect(url_for('login.login'))

        return view(**kwargs)

    return wrapped_view