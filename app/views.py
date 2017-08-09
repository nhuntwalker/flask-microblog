"""Request handlers for the microblog."""
from app import app


@app.route('/')
@app.route('/index')
def index():
    """The home page for the Flask microblog."""
    return "Hello, World!"
