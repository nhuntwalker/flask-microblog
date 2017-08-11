# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Constructor of the login form."""

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

    def check_credentials(self) -> bool:
        """Check credentials for a username/password set."""
        user = User.query.filter_by(
            username=self.username.data
        ).first()
        if not user or not self.password.data or user.password != self.password.data:
            return False
        return True
