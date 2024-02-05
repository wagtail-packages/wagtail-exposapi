from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.snippets.models import get_snippet_models

from exposapi.config import get_wagtail_core_listing_pages_config


def exposapi_view(request):
    if request.GET.get("url"):
        url = request.GET.get("url")
    else:
        url = "http://localhost:8000"

    if request.GET.get("all"):
        all = True
    else:
        all = False

    results = []  # list of tuples (url, name)

    for app in get_wagtail_core_listing_pages_config()["apps"]:
        list_url = f"{url}{reverse(app['listing_name'])}"
        results.append(
            {
                "group": "AdminListingPage",
                "name": f"{app['title']} ({app['listing_name']})",
                "url": list_url,
            }
        )

    configuration = {
        "title": "Wagtail core edit pages",
        "apps": [],
    }

    for a in apps.get_app_configs():
        if hasattr(settings, "DEVTOOLS_APPS_EXCLUDE"):
            if a.name in settings.DEVTOOLS_APPS_EXCLUDE:
                continue
        configuration["apps"].append(
            {
                "app_name": a.label,
                "models": [apps.get_model(a.label, m).__name__ for m in a.models],
            }
        )

    for app in configuration["apps"]:
        models = apps.get_app_config(app["app_name"]).get_models()
        for model in models:
            is_collection = model.__name__ == "Collection"
            is_snippet = model.__name__ in [
                model.__name__ for model in get_snippet_models()
            ]

            if is_collection:
                items = (
                    # don't include the root collection
                    [model.objects.first().get_first_child()]
                    if not all
                    else model.objects.all().exclude(depth=1)
                )

            if is_snippet:
                items = [model.objects.first()] if not all else model.objects.all()

            if not is_collection and not is_snippet:
                # must be some other model that doesn't need special handling
                items = [model.objects.first()] if not all else model.objects.all()

            for item in items:
                if AdminURLFinder().get_edit_url(item):
                    results.append(
                        {
                            "group": "AdminEditPage",
                            "name": f"{model.__name__} ({app['app_name']})",
                            "url": f"{url}{AdminURLFinder().get_edit_url(item)}",
                        }
                    )
                    if hasattr(item, "get_url") and item.get_url():
                        results.append(
                            {
                                "group": "SiteViewPage",
                                "name": f"{model.__name__} ({app['app_name']})",
                                "url": item.get_url(),
                            }
                        )

        sorted_results = sorted(results, key=lambda x: x["group"])

    return JsonResponse(sorted_results, safe=False)
