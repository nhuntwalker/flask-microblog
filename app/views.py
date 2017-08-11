"""Request handlers for the microblog."""
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from app.forms import LoginForm
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
def index() -> LocalStack:
    """The home page for the Flask microblog."""
    user = {'nickname': 'Nick'}
    context = {'title': 'Home', 'user': user, 'posts': POSTS}
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login() -> Union[Response, LocalStack]:
    """View for handling GET and POST requests to the login route."""
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            flash(
                f'Login requested for username: {form.username.data}, password: {form.password.data}, remember_me: {form.remember_me.data}'
            )
            if form.check_credentials():
                session['remember_me'] = form.remember_me.data
                return redirect(url_for('index'))

        flash('Invalid login. Please try again.')

    context = {'title': 'Sign In', 'form': form}
    return render_template('login.html', **context)


@lm.user_loader
def load_user(id: int) -> User:
    """Given an ID, load a user from the database."""
    return User.query.get(int(id))


