# Wagtail Exposapi

Wagtail Exposapi is a Wagtail plugin that provides a JSON API for your Wagtail sites internals.

## Usage Suggestion

When installed a JSON API view will list all:

- admin listing page urls.
- at least one of all edit page urls for installed Wagtail core apps.
- at least one of all edit page type urls for your own models in installed apps.
- at least one of all page type views for your own models in installed apps.

It does this with zero configuration. If need be you can provided configuration to exclude models or apps or provide a full list of apps/models to work with.

With this information it's possible to make a get request to each URL and check the response using various external tools or scripts e.g.

- use a tool like Postman to check the responses.
- create a script to check the responses.
- use a monitoring service to check the responses.
- use a CI/CD pipeline to check the responses.
- and so on.

### Site requirements

If you are checking a site locally it will work best with a full set of data, so it's best to load staging or development site data and the site will need to be running and ready to response to requests.

### Try the package locally

This package has a sandbox site that you can use to try it out locally.

1. Clone the repo
2. Set up a virtual environment
3. Run `pip install -e '.[modeladmin2]'`
4. Run `python manage.py migrate`
5. Run `python manage.py load_fixtures`
6. Run `python manage.py runserver`

Visit `http://localhost:8000/exposapi/` to see the default JSON api endpoint for the sandbox or `http://localhost:8000/exposapi/?all=1` to see all possible urls for the loaded fixtures.

For admin login use `superuser` and `superuser` as the username and password.

## Included Base Command

`BaseResponsesCommand` - A base command that you can extend in your own site to fetch the API data and check the responses.

The default behavior is to report any urls that return a response code other than 200.

You can add options to see more details: `--expanded` includes the 200 responses in the output, `--all` includes all responses endpoints in a site (could be slow depending the size of the size).

Create a new command in your site that extends `BaseResponsesCommand`.

```python
from exposapi.responses_command import BaseResponsesCommand


class Command(BaseResponsesCommand):
    pass
```

For convenience you can add default options to the command so you don't need to type them each time you run the command.

```python
class Command(BaseResponsesCommand):
    # you might want to fetch these from environment variables
    username = "your-login-username"
    password = "your-login-password"
    url = "http://localhost:8000"  # the base url of your site
    login_url = "/admin/login/"  # the login url for your site
```

## Installation

Install the package with pip:

```bash
pip install wagtail-exposapi # coming soon
```

Before it's released you can install it from this repo:

```bash
pip install git+https://github.com/wagtail-packages/wagtail-exposapi.git
```

Add `exposapi` to your `INSTALLED_APPS` in your Django settings file: **make sure you really want to enable it in your production site.** It doesn't really expose anything sensitive but you may not want to expose your site's internals. You could just add this to your development settings or staging site settings.

Update your `urls.py` to include the exposapi urls:

```python
urlpatterns = [
    ...,
    path("exposapi/", include("exposapi.urls")),
    ...,
]
```

## Configuration

If you want to customise the introspection you can provide the configuration shown below.

```python
EXPOSAPI_CONFIG = {
    "base_url": "http://localhost:8000",
    "listing_exclude": [
        "wagtailimages",
        ...,  # these apps won't be included in the listing pages
    ],
    "listing_pages_config": [
        {
            "title": "Search promotions",
            "app_name": "wagtailsearchpromotions",
            "listing_name": "wagtailsearchpromotions:index",
        },
        {
            "title": "Forms",
            "app_name": "wagtailforms",
            "listing_name": "wagtailforms:index",
        },
        ...,  # these will override the introspection for the listing pages
    ],
    "apps_exclude": [
        "wagtailimages",
        ...,  # these apps won't be included in the edit pages
    ],
}
```

## Tested With

- Python 3.8, 3.9, 3.10, 3,11, 3.12
- Django 3.2, 4.0, 4.1, 4.2, 5.0
- Wagtail 4.1, 4.2, 5.0, 5.1, 5.2, 6.0

Wagtail 5.1 can be used with wagtail-modeladmin 1.0.0 and wagtail 5.2+ can be used with wagtail-modeladmin 2.0.0

Model admin is only required if you still use it in your site.
