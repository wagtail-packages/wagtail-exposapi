from django.core.management.base import BaseCommand

import requests


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
        login_handler = LoginHandler(options["url"])
        login_handler.login(options["username"], options["password"])
        if not options["all"]:
            response = login_handler.get_response(f"{options['url']}/exposapi/")
        else:
            response = login_handler.get_response(
                f"{options['url']}/exposapi/?all=true"
            )

        if not response.status_code == 200:
            raise Exception("API view not found")

        resp_200 = []
        resp_404 = []
        resp_500 = []
        resp_302 = []

        for item in response.json():
            response = login_handler.get_response(item["url"])
            if response.status_code == 200:
                if options["expanded"]:
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

        login_handler.logout()


class LoginHandler:
    def __init__(self, url):
        self.url = url
        self._is_authenticated = False
        self.login_url = f"{self.url}/admin/login/"
        self.session = requests.Session()

    def login(self, username, password):
        try:
            login_form = self.session.get(self.login_url)
            if login_form.status_code == 404:
                raise Exception("Login page not found")
        except requests.exceptions.ConnectionError:
            exit("Server not running")

        user = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": login_form.cookies["csrftoken"],
        }
        response = self.session.post(self.login_url, data=user)
        if response.status_code == 200:
            self._is_authenticated = True
            print("Authenticated 🔓")
        return self

    def logout(self):
        self._is_authenticated = False
        self.session = requests.Session()
        print("Logged out 🔒")
        return self

    def get_response(self, url):
        # a request that can be used to make authenticated requests
        # for accessing the wagtail admin pages
        response = self.session.get(url)
        return response

    def is_authenticated(self):
        return self._is_authenticated
