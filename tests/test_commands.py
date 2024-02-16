from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import LiveServerTestCase

import requests
import responses

from exposapi.responses_command import BaseResponsesCommand


class TestCommands(LiveServerTestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username="superuser",
            email="superuser",
            password="superuser",
        )
        user.save()

    @responses.activate
    def test_get_response(self):
        responses.add(
            responses.GET,
            f"{self.live_server_url}/exposapi/",
            status=200,
            json={},
        )

        class MyCommand(BaseResponsesCommand):
            pass

        data = MyCommand().get_response(
            {
                "username": "superuser",
                "password": "superuser",
                "all": False,
                "expanded": False,
                "url": f"{self.live_server_url}",
            },
            requests,
        )

        self.assertEqual(data.status_code, 200)

    @responses.activate
    def test_get_response_not_200(self):
        responses.add(
            responses.GET,
            f"{self.live_server_url}/exposapi/",
            status=404,
        )

        class MyCommand(BaseResponsesCommand):
            pass

        data = MyCommand().get_response(
            {
                "username": "superuser",
                "password": "superuser",
                "all": False,
                "expanded": False,
                "url": f"{self.live_server_url}",
            },
            requests,
        )

        self.assertIsNone(data)

    @responses.activate
    def test_login_action(self):
        responses.add(
            responses.GET,
            f"{self.live_server_url}/admin/login/",
            status=200,
            content_type="text/html",
            headers={"Set-Cookie": "csrftoken=1234567890;"},
        )
        responses.add(
            responses.POST,
            f"{self.live_server_url}/admin/login/",
            status=200,
            content_type="text/html",
            headers={"Set-Cookie": "sessionid=1234567890;"},
        )

        class MyCommand(BaseResponsesCommand):
            pass

        request = MyCommand().login_action(
            {
                "username": "superuser",
                "password": "superuser",
                "all": False,
                "expanded": False,
                "url": f"{self.live_server_url}",
                "login_path": "/admin/login/",
            }
        )

        self.assertIsNotNone(request.cookies.get("sessionid"))

    @responses.activate
    def test_login_action_failed(self):
        responses.add(
            responses.GET,
            f"{self.live_server_url}/admin/login/",
            status=200,
            content_type="text/html",
            headers={"Set-Cookie": "csrftoken=1234567890;"},
        )
        responses.add(
            responses.POST,
            f"{self.live_server_url}/admin/login/",
            status=200,
            content_type="text/html",
        )

        class MyCommand(BaseResponsesCommand):
            pass

        request = MyCommand().login_action(
            {
                "username": "superuser",
                "password": "superuser",
                "all": False,
                "expanded": False,
                "url": f"{self.live_server_url}",
                "login_path": "/admin/login/",
            }
        )

        self.assertIsNone(request)

    @responses.activate
    def test_report(self):
        responses.add(
            responses.GET,
            "http://localhost:8000",
            status=200,
        )
        responses.add(
            responses.GET,
            "http://localhost:8000/not-found/",
            status=404,
        )
        responses.add(
            responses.GET,
            "http://localhost:8000/server-error/",
            status=500,
        )
        responses.add(
            responses.GET,
            "http://localhost:8000/redirect/",
            status=302,
        )

        data_200 = {
            "group": "SiteViewPage",
            "name": "HomePage (home)",
            "url": "http://localhost:8000",
        }
        data_404 = {
            "group": "SiteViewPage",
            "name": "NotFoundPage (home)",
            "url": "http://localhost:8000/not-found/",
        }
        data_500 = {
            "group": "SiteViewPage",
            "name": "ServerErrorPage (home)",
            "url": "http://localhost:8000/server-error/",
        }
        data_302 = {
            "group": "SiteViewPage",
            "name": "RedirectPage (home)",
            "url": "http://localhost:8000/redirect/",
        }

        results = [data_200, data_404, data_500, data_302]
        options = {"expanded": False}

        class MyCommand(BaseResponsesCommand):
            pass

        report = MyCommand().report(requests, results, options)
        self.assertIsNone(report)

    @responses.activate
    def test_report_expanded(self):
        responses.add(
            responses.GET,
            "http://localhost:8000",
            status=200,
        )
        responses.add(
            responses.GET,
            "http://localhost:8000/not-found/",
            status=404,
        )
        responses.add(
            responses.GET,
            "http://localhost:8000/server-error/",
            status=500,
        )
        responses.add(
            responses.GET,
            "http://localhost:8000/redirect/",
            status=302,
        )

        data_200 = {
            "group": "SiteViewPage",
            "name": "HomePage (home)",
            "url": "http://localhost:8000",
        }
        data_404 = {
            "group": "SiteViewPage",
            "name": "NotFoundPage (home)",
            "url": "http://localhost:8000/not-found/",
        }
        data_500 = {
            "group": "SiteViewPage",
            "name": "ServerErrorPage (home)",
            "url": "http://localhost:8000/server-error/",
        }
        data_302 = {
            "group": "SiteViewPage",
            "name": "RedirectPage (home)",
            "url": "http://localhost:8000/redirect/",
        }

        results = [data_200, data_404, data_500, data_302]
        options = {"expanded": True}

        class MyCommand(BaseResponsesCommand):
            pass

        report = MyCommand().report(requests, results, options)
        self.assertIsNone(report)

    @responses.activate
    def test_report_no_results(self):
        results = []
        options = {"expanded": False}

        class MyCommand(BaseResponsesCommand):
            pass

        report = MyCommand().report(requests, results, options)
        self.assertIsNone(report)

    @responses.activate
    def test_report_no_results_expanded(self):
        results = []
        options = {"expanded": True}

        class MyCommand(BaseResponsesCommand):
            pass

        report = MyCommand().report(requests, results, options)
        self.assertIsNone(report)

    @responses.activate
    @patch("exposapi.responses_command.BaseResponsesCommand.login_action")
    @patch("exposapi.responses_command.BaseResponsesCommand.get_response")
    @patch("exposapi.responses_command.BaseResponsesCommand.report")
    def test_handle(self, mock_report, mock_get_response, mock_login_action):
        mock_login_action.return_value = MagicMock()
        mock_get_response.return_value = MagicMock()
        mock_report.return_value = MagicMock()

        class MyCommand(BaseResponsesCommand):
            pass

        MyCommand().handle(
            "http://localhost:8000",
            "http://localhost:8000/admin/login/",
            "superuser",
            "superuser",
            False,
        )

        self.assertTrue(mock_login_action.called)
        self.assertTrue(mock_get_response.called)
        self.assertTrue(mock_report.called)
