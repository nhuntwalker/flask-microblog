"""Request handlers for the microblog."""
from flask import render_template, flash, redirect, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm, RegistrationForm
from app.models import User

from typing import Union
from werkzeug.local import LocalStack
from werkzeug.wrappers import Response


POSTS = [
    {
        'author': {'nickname': 'John'},
        'body': 'Beautiful day in Seattle'
    },
    {
        'author': {'nickname': 'Susan'},
        'body': 'The Avengers movie was so good!'
    },
]


@app.route('/')
@app.route('/index')
@login_required
def index() -> LocalStack:
    """The home page for the Flask microblog."""
    context = {'title': 'Home'}
    if authenticated(g):
        user = {'nickname': g.user.username}
        context['user'] = user
    else:
        context['user'] = None

    context['posts'] = POSTS
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login() -> Union[Response, LocalStack]:
    """View for handling GET and POST requests to the login route."""

    if authenticated(g):
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            if form.check_credentials():
                session['remember_me'] = form.remember_me.data
                user = User.query.filter_by(
                    username=form.username.data
                ).first()
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))

        flash('Invalid login. Please try again.')

    context = {'title': 'Sign In', 'form': form}
    return render_template('login.html', **context)


@app.route('/logout')
def logout() -> LocalStack:
    """Log a user out and remove from global context."""
    logout_user()
    return render_template('logout.html')


@app.route('/register', methods=["GET", "POST"])
def register() -> Response:
    """Register a new user and log them in."""
    if authenticated(g):
        return redirect(url_for('index'))

    form = RegistrationForm()
    if request.method == "POST":
        # create a new user and log them in.
        pass

    context = {'title': "Register New User", 'form': form}
    return render_template('register.html', **context)


@lm.user_loader
def load_user(id: int) -> User:
    """Given an ID, load a user from the database."""
    return User.query.get(int(id))


def authenticated(g_ctx: g) -> bool:
    """Check if the authenticated user is available in the global context."""
    if hasattr(g, 'user') and g.user is not None and g.user.is_authenticated:
        return True
    return False


@app.before_request
def before_request() -> None:
    """Execute this before every request."""
    g.user = current_user
