from django.contrib.auth.models import User
from django.test import TestCase

import requests
import responses

from exposapi.auth_handler import LoginHandler

# from sandbox.settings.base import STATICFILES_STORAGE


class TestAuthHandler(TestCase):
    @responses.activate
    def test_login_handler(self):
        responses.add(
            responses.GET,
            "http://localhost:8000/admin/login/",
            status=200,
            content_type="text/html",
        )

        login_handler = LoginHandler("http://localhost:8000")
        self.assertIsInstance(login_handler, LoginHandler)
        self.assertEqual(login_handler.url, "http://localhost:8000")
        self.assertFalse(login_handler.is_authenticated())
        self.assertEqual(login_handler.login_url, "http://localhost:8000/admin/login/")
        self.assertIsInstance(login_handler.session, requests.Session)

    @responses.activate
    def test_get_response(self):
        responses.add(
            responses.GET,
            "http://localhost:8000",
            status=200,
            content_type="text/html",
        )

        login_handler = LoginHandler("http://localhost:8000")
        response = login_handler.get_response("http://localhost:8000")
        self.assertIsInstance(response, requests.Response)

    @responses.activate
    def test_login_server_check(self):
        responses.add(
            responses.GET,
            "http://localhost:8000/admin/login/",
            status=ConnectionError,
            content_type="text/html",
        )

        login_handler = LoginHandler("http://localhost:8000")
        with self.assertRaises(Exception):
            login_handler.login("superuser", "superuser")

        responses.add(
            responses.GET,
            "http://localhost:8000/admin/login/",
            status=404,
            content_type="text/html",
        )

        login_handler = LoginHandler("http://localhost:8000")
        with self.assertRaises(Exception) as e:
            login_handler.login("superuser", "superuser")
        self.assertEqual(str(e.exception), "Login page not found")

    @responses.activate
    # @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_login(self):
        user = User.objects.create_user(
            username="superuser",
            email="superuser@example.com",
            password="superuser",
            is_superuser=True,
        )
        user.save()

        responses.add(
            responses.GET,
            "http://localhost:8000/admin/login/",
            status=200,
            content_type="text/html",
            headers={"Set-Cookie": "csrftoken=1234567890;"},
        )
        responses.add(
            responses.POST,
            "http://localhost:8000/admin/login/",
            status=200,
            content_type="text/html",
        )

        login_handler = LoginHandler("http://localhost:8000")
        login_handler.login("superuser", "superuser")
        self.assertTrue(login_handler.is_authenticated())

    @responses.activate
    def test_logout(self):
        responses.add(
            responses.GET,
            "http://localhost:8000/admin/login/",
            status=200,
            content_type="text/html",
            headers={"Set-Cookie": "csrftoken=1234567890;"},
        )
        responses.add(
            responses.POST,
            "http://localhost:8000/admin/login/",
            status=200,
            content_type="text/html",
        )

        login_handler = LoginHandler("http://localhost:8000")
        login_handler.login("superuser", "superuser")
        self.assertTrue(login_handler.is_authenticated())
        login_handler.logout()
        self.assertFalse(login_handler.is_authenticated())
