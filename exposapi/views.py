from django.apps import apps
from django.http import JsonResponse
from django.urls import reverse

from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.snippets.models import get_snippet_models

from exposapi.config import get_config, get_wagtail_core_listing_pages_config


def app_config(exclude_apps) -> list:
    apps_config = []

    for app in apps.get_app_configs():
        if app.name not in exclude_apps:
            apps_config.append(
                {
                    "app_name": app.label,
                    "models": [
                        apps.get_model(app.label, m).__name__ for m in app.models
                    ],
                }
            )

    return apps_config


def app_listings(url) -> list:
    results = []

    for app in get_wagtail_core_listing_pages_config()["apps"]:
        list_url = f"{url}{reverse(app['listing_name'])}"
        results.append(
            {
                "group": "AdminListingPage",
                "name": f"{app['title']} ({app['listing_name']})",
                "url": list_url,
            }
        )

    return results


def is_collection(model) -> bool:
    return model.__name__ == "Collection"


def is_snippet(model) -> bool:
    return model.__name__ in [model.__name__ for model in get_snippet_models()]


def get_admin_edit_url(item) -> str:
    return AdminURLFinder().get_edit_url(item)


def get_item_url(item) -> str:
    return item.get_url() if hasattr(item, "get_url") and item.get_url() else None


def item_result(app, model, item_url):
    return {
        "group": "SiteViewPage",
        "name": f"{model.__name__} ({app['app_name']})",
        "url": item_url,
    }


def admin_edit_result(url, app, model, admin_edit_url):
    return {
        "group": "AdminEditPage",
        "name": f"{model.__name__} ({app['app_name']})",
        "url": f"{url}{admin_edit_url}",
    }


def exposapi_view(request) -> JsonResponse:
    config = get_config()

    if config["base_url"]:
        url = config["base_url"]
    else:
        url = request.build_absolute_uri("/")

    all = True if request.GET.get("all") else False

    results_cached = app_listings(url)

    for app in app_config(exclude_apps=config["apps_exclude"]):
        models = apps.get_app_config(app["app_name"]).get_models()
        for model in models:
            if is_collection(model):
                items = (
                    # not the root collection
                    [model.objects.first().get_first_child()]
                    if not all
                    else model.objects.all().exclude(depth=1)
                )

            if is_snippet(model):
                items = [model.objects.first()] if not all else model.objects.all()

            if not is_collection(model) and not is_snippet(model):
                items = [model.objects.first()] if not all else model.objects.all()

            for item in items:
                admin_edit_url = get_admin_edit_url(item)
                item_url = get_item_url(item)

                if admin_edit_url:
                    results_cached.append(
                        admin_edit_result(url, app, model, admin_edit_url)
                    )
                    if item_url:
                        results_cached.append(item_result(app, model, item_url))

    return JsonResponse(
        sorted(results_cached, key=lambda x: x["group"]),
        safe=False,
    )
