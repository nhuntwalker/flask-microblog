# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app import db


class User(db.Model):
    """The User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(length=80), index=True, unique=True)
    password = db.Column(db.Unicode)

    def __repr__(self):
        """String representation of the User model."""
        return '<User {self.username} | id: {self.id}>'
