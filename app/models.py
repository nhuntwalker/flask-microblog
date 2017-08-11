# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import db


class User(db.Model):
    """The User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(length=80), index=True, unique=True)
    password = db.Column(db.Unicode)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        """String representation of the User model."""
        return f'<User {self.username} | id: {self.id}>'


class Post(db.Model):
    """The Post model."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, unique=True)
    body = db.Column(db.Unicode)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """String representation of the Post model."""
        return f'<Post {self.title}>'
