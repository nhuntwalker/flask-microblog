# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import db
from typing import Union


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)


class User(db.Model):
    """The User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(length=80), index=True, unique=True)
    password = db.Column(db.Unicode)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.Unicode)
    last_seen = db.Column(db.DateTime)
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

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

    def follow(self, user):
        """Follow a new user."""
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        """Unfollow one of an existing set of users."""
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user) -> bool:
        """Check if a given user is being followed."""
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """Retrieve all of the posts from users this user follows."""
        return Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        ).order_by(
            Post.timestamp.desc()
        )


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
