# -*- coding: utf-8 -*-
#!/usr/bin/env python
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


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


class RegistrationForm(FlaskForm):
    """Constructor of the registration form."""

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])


class ProfileForm(FlaskForm):
    """Constructor of the form for editing profiles."""

    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me')

    def __init__(self, original_username, *args, **kwargs) -> None:
        """Form constructor, modified to preserve original username."""
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate(self) -> bool:
        """Validate the form, paying special attention to duplicate names."""
        if not FlaskForm.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        user_exists = User.query.filter_by(username=self.username.data).first()
        if user_exists:
            self.username.errors.append("This username already exists.")
            return False
        return True


class PostForm(FlaskForm):
    """Constructor for a form for adding new posts."""

    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()])
