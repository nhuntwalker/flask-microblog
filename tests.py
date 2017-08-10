# -*- coding: utf-8 -*-
#!flask/bin/python
import unittest

from app import app


class TestCase(unittest.TestCase):
    """The test cases for this app."""

    def setUp(self):
        """."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_route_shows_username(self):
        """."""
        response = self.client.get('/')
        self.assertTrue(
            b'Nick' in response.data
        )

if __name__ == '__main__':
    unittest.main()
