"""Request handlers for the microblog."""
from flask import render_template
from app import app


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
