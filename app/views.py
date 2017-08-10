"""Request handlers for the microblog."""
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


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
def index():
    """The home page for the Flask microblog."""
    user = {'nickname': 'Nick'}
    return render_template('index.html', title='Home', user=user, posts=POSTS)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """View for handling GET and POST requests to the login route."""
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
