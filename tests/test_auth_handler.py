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

    # @responses.activate
    # @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    # def test_login(self):
    #     c = self.client.get("http://localhost:8000/admin/login/")
    #     self.assertEqual(c.status_code, 200)
    #     print(c.__dict__)

    #     responses.add(
    #         responses.POST,
    #         "http://localhost:8000/admin/login/",
    #         status=200,
    #         content_type="text/html",
    #     )
