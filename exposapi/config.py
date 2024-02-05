from django.apps import apps
from django.conf import settings


LISTING_PAGES_CONFIG = [
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
    {
        "title": "Redirects",
        "app_name": "wagtailredirects",
        "listing_name": "wagtailredirects:index",
    },
    {
        "title": "Users",
        "app_name": "wagtailusers",
        "listing_name": "wagtailusers_users:index",
    },
    {
        "title": "Snippets",
        "app_name": "wagtailsnippets",
        "listing_name": "wagtailsnippets:index",
    },
    {
        "title": "Documents",
        "app_name": "wagtaildocs",
        "listing_name": "wagtaildocs:index",
    },
    {
        "title": "Images",
        "app_name": "wagtailimages",
        "listing_name": "wagtailimages:index",
    },
    {
        "title": "Search",
        "app_name": "wagtailsearch",
        "listing_name": "wagtailadmin_pages:search",
    },
    {
        "title": "Styleguide",
        "app_name": "wagtailstyleguide",
        "listing_name": "wagtailstyleguide",
    },
    {
        "title": "Sites",
        "app_name": "wagtailsites",
        "listing_name": "wagtailsites:index",
    },
    {
        "title": "Dashboard",
        "app_name": None,
        "listing_name": "wagtailadmin_home",
    },
    {
        "title": "Collections",
        "app_name": None,
        "listing_name": "wagtailadmin_collections:index",
    },
    {
        "title": "Login",
        "app_name": None,
        "listing_name": "wagtailadmin_login",
    },
    {
        "title": "Password reset",
        "app_name": None,
        "listing_name": "wagtailadmin_password_reset",
    },
    {
        "title": "Reports Locked Pages",
        "app_name": None,
        "listing_name": "wagtailadmin_reports:locked_pages",
    },
    {
        "title": "Reports Aging Pages",
        "app_name": None,
        "listing_name": "wagtailadmin_reports:aging_pages",
    },
    {
        "title": "Reports Site History",
        "app_name": None,
        "listing_name": "wagtailadmin_reports:site_history",
    },
    {
        "title": "Reports Workflow",
        "app_name": None,
        "listing_name": "wagtailadmin_reports:workflow",
    },
    {
        "title": "Reports Workflow Tasks",
        "app_name": None,
        "listing_name": "wagtailadmin_reports:workflow_tasks",
    },
    {
        "title": "Reports Workflows",
        "app_name": None,
        "listing_name": "wagtailadmin_workflows:index",
    },
    {
        "title": "Groups",
        "app_name": None,
        "listing_name": "wagtailusers_groups:index",
    },
]


def get_listing_pages_config():
    return LISTING_PAGES_CONFIG


def get_wagtail_core_listing_pages_config():
    configuration = {
        "title": "Wagtail core listing pages",
        "apps": [],
    }

    for item in get_listing_pages_config():
        # if not item["listing_name"]: # TODO decide if this is required, do some testing on real data
        #     continue
        if hasattr(settings, "DEVTOOLS_LISTING_EXCLUDE"):
            if item["listing_name"] in settings.DEVTOOLS_LISTING_EXCLUDE:
                continue
        configuration["apps"].append(
            {
                "title": item["title"],
                "app_name": item["app_name"],
                "listing_name": item["listing_name"],
            }
        )

    return configuration
