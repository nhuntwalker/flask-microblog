"""Request handlers for the microblog."""
from app import app, db, lm
from app.forms import LoginForm, RegistrationForm, ProfileForm, PostForm
from app.models import User, Post
from config import POSTS_PER_PAGE
from datetime import datetime
from flask import (
    render_template, flash, redirect,
    url_for, request, g, session
)
from flask_login import login_user, logout_user, current_user, login_required

from typing import Union
from werkzeug.local import LocalStack
from werkzeug.wrappers import Response


@app.route('/', methods=['GET', 'POST'])
@app.route('/posts/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1) -> Union[LocalStack, Response]:
    """The home page for the Flask microblog."""
    form = PostForm()
    if form.validate_on_submit():
        existing_post = Post.query.filter_by(title=form.title.data).first()
        if not existing_post:
            post = Post(
                title=form.title.data,
                body=form.body.data,
                timestamp=datetime.utcnow(),
                user_id=g.user.id
            )
            db.session.add(post)
            db.session.commit()
        return redirect(url_for('index'))

    user = {'nickname': g.user.username}
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)

    context = {
        'title': 'Home',
        'user': user,
        'posts': posts,
        'form': form
    }
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
def register() -> Union[LocalStack, Response]:
    """Register a new user and log them in."""
    if authenticated(g):
        return redirect(url_for('index'))

    form = RegistrationForm()
    context = {'title': "Register New User", 'form': form}

    if request.method == "POST":
        # create a new user and log them in.
        if form.validate_on_submit():
            username = form.username.data
            user_exists = User.query.filter_by(username=username).first()
            if user_exists:
                flash('This user already exists.')
                return render_template('register.html', **context)
            pw1 = form.password.data
            pw2 = form.password2.data
            if pw1 != pw2:
                flash("Passwords don't match")
                return render_template('register.html', **context)
            new_user = User(
                username=username, password=pw1
            )
            db.session.add(new_user)
            db.session.commit()
            # the new user will follow themselves
            new_user.follow(new_user)
            db.session.add(new_user)
            dbsession.commit()
            login_user(new_user)
            return redirect(url_for('index'))

    return render_template('register.html', **context)


@app.route('/profile/<username>')
@app.route('/profile/<username>/<int:page>')
@login_required
def profile(username, page=1) -> Union[LocalStack, Response]:
    """View for a user's profile."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    context = {'user': user, 'posts': posts}
    return render_template('profile.html', **context)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile() -> Union[LocalStack, Response]:
    """View for editing a user's profile."""
    form = ProfileForm(g.user.username)
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    context = {'form': form}
    return render_template('edit_profile.html', **context)


@app.route('/follow/<username>')
@login_required
def follow(username) -> Response:
    """For one user to follow another."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('index'))
    if user == g.user:
        return redirect(url_for('profile', username=username))
    u = g.user.follow(user)
    if not u:
        return redirect(url_for('profile', username=username))
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('profile', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username) -> Response:
    """For one user to unfollow another."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('index'))
    if user == g.user:
        return redirect(url_for('profile', username=username))
    u = g.user.unfollow(user)
    if not u:
        return redirect(url_for('profile', username=username))
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('profile', username=username))


@app.errorhandler(404)
def not_found_error(error) -> LocalStack:
    """View for a 404 error."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error) -> LocalStack:
    """View for a 500 error."""
    db.session.rollback()
    return render_template('500.html'), 500


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
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
