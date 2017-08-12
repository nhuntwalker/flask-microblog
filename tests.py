# -*- coding: utf-8 -*-
#!flask/bin/python
from app import app, models, db
from bs4 import BeautifulSoup as Soup
import config
import os
import unittest



class TestCase(unittest.TestCase):
    """The test cases for this app."""

    def setUp(self) -> None:
        """."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = config.TEST_DATABASE_URI
        db.create_all()
        self.client = app.test_client()

    def tearDown(self) -> None:
        """."""
        db.session.remove()
        db.drop_all()

    def get_token(self, url) -> None:
        """Retrieve the csrf token from url."""
        response = self.client.get('/login')
        html = Soup(response.data, 'html.parser')
        token = html.find('input', {'name': 'csrf_token'}).get('value')
        return token

    def create_user(self) -> models.User:
        """."""
        new_user = models.User(username='flerg', password='theblerg')
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def authenticate_user(self, user) -> None:
        """."""
        self.client.post('/login', data={
            'username': user.username,
            'password': user.password,
            'csrf_token': self.get_token('/login')
        })

    def test_unauthenticated_home_route_redirects_to_login(self) -> None:
        """."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            'http://localhost/login' in response.location
        )

    def test_login_route_shows_post_form_with_csrf_token(self) -> None:
        """."""
        response = self.client.get('/login')
        html = Soup(response.data, 'html.parser')
        self.assertIsNotNone(html.find('form', {'name': 'login_form'}))
        form = html.find('form', {'name': 'login_form'})
        self.assertTrue(form.attrs['method'] == 'POST')
        self.assertIsNotNone(html.find('input', {'name': 'csrf_token'}))
        self.assertIsNotNone(html.find('input', {'name': 'username'}))
        self.assertIsNotNone(html.find('input', {'name': 'password'}))

    def test_login_route_post_request_no_creds_lands_on_login_page(self) -> None:
        """."""
        response = self.client.post('/login')
        html = Soup(response.data, 'html.parser')
        self.assertIsNotNone(html.find('form', {'name': 'login_form'}))

    def test_login_route_post_request_nonexistent_creds_lands_on_login_page(self) -> None:
        """."""
        response = self.client.post('/login', data={
            'username': 'flerg',
            'password': 'theblerg',
            'csrf_token': self.get_token('/login')
        })
        html = Soup(response.data, 'html.parser')
        self.assertIsNotNone(html.find('form', {'name': 'login_form'}))

    def test_login_route_post_bad_password_lands_on_login_page(self) -> None:
        """."""
        self.create_user()
        response = self.client.post('/login', data={
            'username': 'flerg',
            'password': 'tugboat',
            'csrf_token': self.get_token('/login')
        })
        html = Soup(response.data, 'html.parser')
        self.assertIsNotNone(html.find('form', {'name': 'login_form'}))

    def test_login_route_post_good_creds_redirects_to_home(self) -> None:
        """."""
        user = self.create_user()
        response = self.client.post('/login', data={
            'username': user.username,
            'password': user.password,
            'csrf_token': self.get_token('/login')
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            'http://localhost/' == response.location
        )

    def test_authenticated_user_sees_homepage(self) -> None:
        """."""
        user = self.create_user()
        self.client.post('/login', data={
            'username': user.username,
            'password': user.password,
            'csrf_token': self.get_token('/login')
        })
        response = self.client.get('/')
        html = Soup(response.data, 'html.parser')
        self.assertIsNotNone(html.find('a', {'href': '/logout'}))

    def test_registration_adds_new_user(self) -> None:
        """."""
        self.client.post('/register', data={
            'username': 'bobberton',
            'password': 'bigbillybob',
            'password2': 'bigbillybob',
            'csrf_token': self.get_token('/register')
        })
        query = db.session.query(models.User)
        self.assertTrue(query.count() == 1)

    def test_unauthenticated_user_cannot_visit_profile_and_redirects_to_login(self) -> None:
        """."""
        user = self.create_user()
        response = self.client.get(f'/profile/{user.username}')
        self.assertTrue(response.status_code == 302)
        self.assertTrue(
            'http://localhost/login' in response.location
        )

    def test_auth_user_can_visit_profile(self) -> None:
        """."""
        user = self.create_user()
        self.authenticate_user(user)
        response = self.client.get(f'/profile/{user.username}')
        html = Soup(response.data, 'html.parser')
        h1 = html.find('h1')
        self.assertTrue(h1.text == f'User: {user.username}')


if __name__ == '__main__':
    unittest.main()
