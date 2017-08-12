# -*- coding: utf-8 -*-
#!flask/bin/python
from app import app
from bs4 import BeautifulSoup as Soup
import unittest


class TestCase(unittest.TestCase):
    """The test cases for this app."""

    def setUp(self) -> None:
        """."""
        app.config['TESTING'] = True
        self.client = app.test_client()

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

if __name__ == '__main__':
    unittest.main()
