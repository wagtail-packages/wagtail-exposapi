from .base import *  # noqa: F403, F401

EXPOSAPI_CONFIG = {
    "base_url": WAGTAILADMIN_BASE_URL,  # noqa: F405
    "listing_exclude": [
        # app names e.g. "wagtailsearchpromotions",
        "wagtailimages",
    ],
    "listing_pages_config": [],
    "apps_exclude": [],
}
