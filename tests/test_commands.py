from django.contrib.auth.models import User
from django.test import LiveServerTestCase

import requests
import responses

from exposapi.responses_command import BaseResponsesCommand


class TestCommands(LiveServerTestCase):
    @responses.activate
    def test_command_handle(self):
        user = User.objects.create_user(
            username="superuser",
            email="superuser@example.com",
            password="superuser",
            is_superuser=True,
        )
        user.save()

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
        responses.add(
            responses.GET,
            f"{self.live_server_url}/exposapi/",
            status=200,
            json={},
        )

        class Cmd(BaseResponsesCommand):
            pass

        options = {
            "username": "superuser",
            "password": "superuser",
            "all": False,
            "expanded": False,
            "url": f"{self.live_server_url}",
        }

        Cmd().handle(**options)

        # login action
        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(
            responses.calls[0].request.url, f"{self.live_server_url}/admin/login/"
        )
        self.assertEqual(responses.calls[0].request.method, "GET")
        self.assertEqual(responses.calls[0].response.status_code, 200)
        self.assertEqual(
            responses.calls[1].request.url, f"{self.live_server_url}/admin/login/"
        )
        self.assertEqual(responses.calls[1].request.method, "POST")
        self.assertEqual(responses.calls[1].response.status_code, 200)

        # get data
        self.assertEqual(
            responses.calls[2].request.url, f"{self.live_server_url}/exposapi/"
        )
        self.assertEqual(responses.calls[2].request.method, "GET")
        self.assertEqual(responses.calls[2].response.status_code, 200)
        self.assertEqual(responses.calls[2].response.json(), {})

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

        class Cmd(BaseResponsesCommand):
            pass

        cmd = Cmd()
        report = cmd.report(requests, [data_200, data_404, data_500, data_302], False)
        self.assertIsNone(report)
