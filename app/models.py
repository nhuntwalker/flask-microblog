# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import db


class User(db.Model):
    """The User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(length=80), index=True, unique=True)
    password = db.Column(db.Unicode)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.Unicode)
    last_seen = db.Column(db.DateTime)

    def __repr__(self) -> str:
        """String representation of the User model."""
        return f'<User {self.username} | id: {self.id}>'

    @property
    def is_authenticated(self) -> bool:
        """Whether or not the user is authenticated."""
        return True

    @property
    def is_active(self) -> bool:
        """Whether or not the user is active."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Whether or not the user is anonymous."""
        return False

    def get_id(self) -> str:
        """Retrieve the ID for this user."""
        return str(self.id)


class Post(db.Model):
    """The Post model."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, unique=True)
    body = db.Column(db.Unicode)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        """String representation of the Post model."""
        return f'<Post {self.title}>'
