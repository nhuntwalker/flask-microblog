# -*- coding: utf-8 -*-
#!flask/bin/python
from app import app, models, db
from bs4 import BeautifulSoup as Soup
import config
from datetime import datetime, timedelta
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

    def setup_users_with_following(self) -> list:
        """."""
        u1 = models.User(username="john", password='johnson')
        u2 = models.User(username="sue", password='susanna')
        db.session.add_all([u1, u2])
        db.session.commit()

        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()
        return u1, u2


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

    def test_nonexistent_profiles_redirect_to_home(self) -> None:
        """."""
        user = self.create_user()
        self.authenticate_user(user)
        response = self.client.get(f'/profile/potato')
        self.assertTrue(response.location == 'http://localhost/')

    def test_unfollow_returns_none_when_not_following(self):
        """."""
        u1 = models.User(username="john", password='johnson')
        u2 = models.User(username="sue", password='susanna')
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertIsNone(u1.unfollow(u2))

    def test_follow_returns_none_when_already_following(self):
        """."""
        u1, u2 = self.setup_users_with_following()
        self.assertIsNone(u1.follow(u2))

    def test_follow_adds_one_to_followed_followers_count(self):
        """."""
        u1, u2 = self.setup_users_with_following()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'sue')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

    def test_unfollow_removes_one_from_followed_followers_count(self):
        """."""
        u1, u2 = self.setup_users_with_following()
        self.assertIsNotNone(u1.unfollow(u2))
        db.session.add(u1)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # make four users
        u1 = models.User(username='john', password='tugboat')
        u2 = models.User(username='susan', password='tugboat')
        u3 = models.User(username='mary', password='tugboat')
        u4 = models.User(username='david', password='tugboat')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        # make four posts
        utcnow = datetime.utcnow()
        p1 = models.Post(title="post from john", user_id=u1.id, timestamp=utcnow + timedelta(seconds=1))
        p2 = models.Post(title="post from susan", user_id=u2.id, timestamp=utcnow + timedelta(seconds=2))
        p3 = models.Post(title="post from mary", user_id=u3.id, timestamp=utcnow + timedelta(seconds=3))
        p4 = models.Post(title="post from david", user_id=u4.id, timestamp=utcnow + timedelta(seconds=4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        # setup the followers
        u1.follow(u1)  # john follows himself
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u2)  # susan follows herself
        u2.follow(u3)  # susan follows mary
        u3.follow(u3)  # mary follows herself
        u3.follow(u4)  # mary follows david
        u4.follow(u4)  # david follows himself
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertTrue(len(f1), 3)
        self.assertTrue(len(f2), 2)
        self.assertTrue(len(f3), 2)
        self.assertTrue(len(f4), 1)
        self.assertTrue(f1, [p4, p2, p1])
        self.assertTrue(f2, [p3, p2])
        self.assertTrue(f3, [p4, p3])
        self.assertTrue(f4, [p4])

if __name__ == '__main__':
    unittest.main()
