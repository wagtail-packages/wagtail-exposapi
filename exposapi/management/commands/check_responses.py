from django.core.management.base import BaseCommand

import requests

# Untested code, provided as a convenience for development
# and testing purposes only.
# Why not write your own app to do this?
# You can write it in any language you like.


class Command(BaseCommand):
    help = "Check responses of API views."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Username to use for login.",
            default="superuser",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Password to use for login.",
            default="superuser",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Check all API views (slow).",
        )
        parser.add_argument(
            "--url",
            type=str,
            help="The url to test (default=http://localhost:8000)",
            default="http://localhost:8000",
        )
        parser.add_argument(
            "--expanded",
            action="store_true",
            help="Show expanded output.",
        )

    def handle(self, *args, **options):
        request = self.login_action(
            options["url"],
            options["username"],
            options["password"],
        )
        data = (
            request.get(f"{options['url']}/exposapi/")
            if not options["all"]
            else request.get(f"{options['url']}/exposapi/?all=true")
        )

        if not data.status_code == 200:
            exit("Is the server running?")
        else:
            self.report(request, data.json(), options["expanded"])

    def login_action(self, url, username, password):
        request = requests.Session()
        login_url = f"{url}/admin/login/"
        login_form = request.get(login_url)
        csrftoken = login_form.cookies["csrftoken"]
        user = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": csrftoken,
        }
        response = request.post(login_url, data=user)

        if response.status_code == 200:
            print("Authenticated 🔓")
            return request
        else:
            exit("Authentication failed")

    def report(self, request, data, expanded):
        resp_200 = []
        resp_404 = []
        resp_500 = []
        resp_302 = []

        for item in data:
            response = request.get(item["url"])
            if response.status_code == 200:
                if expanded:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{item['name']} - {item['url']} ({response.status_code})"
                        )
                    )
                resp_200.append(item["url"])
            elif response.status_code == 404:
                self.stdout.write(
                    self.style.WARNING(
                        f"{item['name']} - {item['url']} ({response.status_code})"
                    )
                )
                resp_404.append(item["url"])
            elif response.status_code == 500:
                self.stdout.write(
                    self.style.ERROR(
                        f"{item['name']} - {item['url']} ({response.status_code})"
                    )
                )
                resp_500.append(item["url"])
            elif response.status_code == 302:
                self.stdout.write(
                    f"{item['name']} - {item['url']} ({response.status_code})"
                )
                resp_302.append(item["url"])
