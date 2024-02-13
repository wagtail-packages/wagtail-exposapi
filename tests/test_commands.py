from django.contrib.auth.models import User
from django.test import LiveServerTestCase

import requests
import responses

from exposapi.responses.management.commands.check_responses import (
    Command as CheckResponsesCommand,
)


class TestCommands(LiveServerTestCase):
    @responses.activate
    def test_command_login_action(self):
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

        response = CheckResponsesCommand().login_action(
            self.live_server_url,
            "superuser",
            "superuser",
        )
        self.assertIsInstance(response, requests.Session)
