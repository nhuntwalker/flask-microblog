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

    def test_hello_world(self):
        """."""
        response = self.client.get('/')
        self.assertEqual(
            b'Hello, World!', response.data
        )

if __name__ == '__main__':
    unittest.main()
