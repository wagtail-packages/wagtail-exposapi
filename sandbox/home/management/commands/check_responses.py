from exposapi.responses_command import BaseResponsesCommand


class Command(BaseResponsesCommand):
    username = "superuser"
    password = "superuser"
    url = "http://localhost:8000"
