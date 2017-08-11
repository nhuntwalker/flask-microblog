"""Request handlers for the microblog."""
from flask import render_template, flash, redirect, url_for
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
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f'Login requested for username: {form.username.data}, password: {form.password.data}, remember_me: {form.remember_me.data}'
        )
        return redirect(url_for('index'))
    context = {'title': 'Sign In', 'form': form}
    return render_template('login.html', **context)


@lm.user_loader
def load_user(id: int) -> User:
    """Given an ID, load a user from the database."""
    return User.query.get(int(id))
