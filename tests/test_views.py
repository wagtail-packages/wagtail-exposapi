from django.test import RequestFactory, TestCase, override_settings

from exposapi.views import (  # item_result,
    admin_edit_result,
    app_config,
    app_listings,
    exposapi_view,
    get_admin_edit_url,
    get_item_url,
    is_collection,
    is_snippet,
    item_result,
)


class TestMethod(TestCase):
    def test_app_config(self):
        """Test app_config."""
        exclude_apps = []
        apps_config = app_config(exclude_apps)

        self.assertIsInstance(apps_config, list)

        keys = [app["app_name"] for app in apps_config]
        self.assertIn("wagtailimages", keys)

    def test_app_config_exclude(self):
        """Test app_config with exclude_apps."""
        exclude_apps = ["sandbox_home"]
        apps_config = app_config(exclude_apps)

        self.assertIsInstance(apps_config, list)

        keys = [app["app_name"] for app in apps_config]
        self.assertNotIn("wagtailimiages", keys)

    def test_app_listings(self):
        """Test app_listings."""
        url = "https://example.com"
        results = app_listings(url)

        self.assertIsInstance(results, list)
        self.assertEqual(results[0]["group"], "AdminListingPage")
        self.assertEqual(
            results[0]["name"], "Search promotions (wagtailsearchpromotions:index)"
        )
        self.assertEqual(results[0]["url"], "https://example.com/admin/searchpicks/")

    def test_is_collection(self):
        """Test is_collection."""
        from wagtail.models import Collection

        self.assertTrue(is_collection(Collection))

    def test_is_snippet(self):
        """Test is_snippet."""
        from sandbox.home.models import TestSnippetOne

        self.assertTrue(is_snippet(TestSnippetOne))

    def test_get_admin_edit_url(self):
        """Test get_admin_edit_url."""
        from sandbox.home.models import HomePage

        url = get_admin_edit_url(HomePage.objects.first())
        self.assertEqual(url, "/admin/pages/3/edit/")

    def test_get_item_url(self):
        """Test get_item_url."""
        from sandbox.home.models import HomePage

        url = get_item_url(HomePage.objects.first())
        print(url)
        self.assertEqual(url, "http://localhost/")

    def test_item_result(self):
        """Test item_result."""
        from sandbox.home.models import HomePage

        app = {"app_name": "home"}
        model = HomePage
        item_url = "http://localhost:8000/"

        result = item_result(app, model, item_url)
        self.assertEqual(result["group"], "SiteViewPage")
        self.assertEqual(result["name"], "HomePage (home)")
        self.assertEqual(result["url"], "http://localhost:8000/")

    def test_admin_edit_result(self):
        """Test admin_edit_result."""
        from sandbox.home.models import HomePage

        url = "https://example.com"
        app = {"app_name": "home"}
        model = HomePage
        admin_edit_url = "/admin/pages/3/edit/"

        result = admin_edit_result(url, app, model, admin_edit_url)
        self.assertEqual(result["group"], "AdminEditPage")
        self.assertEqual(result["name"], "HomePage (home)")
        self.assertEqual(result["url"], "https://example.com/admin/pages/3/edit/")


class TestViews(TestCase):
    def test_exposapi_view(self):
        """Test exposapi_view."""
        request = RequestFactory().get("/")
        response = exposapi_view(request)

        self.assertEqual(response.status_code, 200)

    def test_exposapi_view_all(self):
        """Test exposapi_view with all models."""
        request = RequestFactory().get("/?all=true")
        response = exposapi_view(request)

        self.assertEqual(response.status_code, 200)

    @override_settings(EXPOSAPI_CONFIG={"base_url": "https://example.com"})
    def test_exposapi_view_base_url(self):
        """Test exposapi_view with base_url."""
        request = RequestFactory().get("/")
        response = exposapi_view(request)

        self.assertEqual(response.status_code, 200)
