# -*- coding: utf-8 -*-
#!flask/bin/python
import unittest

from app import app


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

if __name__ == '__main__':
    unittest.main()
