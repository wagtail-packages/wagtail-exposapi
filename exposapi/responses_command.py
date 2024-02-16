from django.core.management.base import BaseCommand

import requests


class BaseResponsesCommand(BaseCommand):
    help = "Check responses of API views."

    username = "superuser"
    password = "superuser"
    url = "http://localhost:8000"
    login_path = "/admin/login/"

    # Extend this command class to use it in your own site.

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument(
            "--username",
            type=str,
            help="Username to use for login.",
            default=self.username,
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Password to use for login.",
            default=self.password,
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
            default=self.url,
        )
        parser.add_argument(
            "--login-path",
            type=str,
            help="The login url (default=http://localhost:8000/admin/login/)",
            default=self.login_path,
        )
        parser.add_argument(
            "--expanded",
            action="store_true",
            help="Show expanded output.",
        )

    def handle(self, *args, **options):
        request = self.login_action(options)
        data = self.get_response(options, request)
        results = data.json() if data else None
        self.report(request, results, options)

    def get_response(self, options, request):
        data = (
            request.get(f"{options['url']}/exposapi/?all=true")
            if hasattr(options, "all") and options["all"]
            else request.get(f"{options['url']}/exposapi/")
        )

        if not data.status_code == 200:
            self.stdout.write(self.style.ERROR("API not found"))
            return

        return data

    def login_action(self, options):
        request = requests.Session()
        login_form_url = f"{options['url']}{options['login_path']}"
        form = request.get(login_form_url)
        csrftoken = form.cookies["csrftoken"]

        user = {
            "username": options["username"],
            "password": options["password"],
            "csrfmiddlewaretoken": csrftoken,
        }
        request.post(login_form_url, data=user)

        if request is None or not request.cookies.get("sessionid"):
            self.stdout.write(self.style.ERROR("Authentication failed"))
            return

        return request

    def report(self, request, results, options):

        resp_200 = []
        resp_404 = []
        resp_500 = []
        resp_302 = []

        for item in results:
            response = request.get(item["url"])
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
