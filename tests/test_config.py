from django.test import SimpleTestCase, override_settings

from exposapi.config import (
    LISTING_PAGES_CONFIG,
    get_config,
    get_wagtail_core_listing_pages_config,
)


class TestConfig(SimpleTestCase):
    def test_get_config_default(self):
        """Test get_config with default settings, where EXPOSAPI_CONFIG is not set."""

        config = get_config()

        self.assertEqual(config["base_url"], "")
        self.assertEqual(config["listing_exclude"], [])
        self.assertIsInstance(config["listing_pages_config"], list)
        self.assertEqual(config["apps_exclude"], [])

        app_listing = config["listing_pages_config"]
        listing_pages_config = LISTING_PAGES_CONFIG
        self.assertEqual(len(app_listing), len(listing_pages_config))

    @override_settings(EXPOSAPI_CONFIG={})
    def test_get_config_empty(self):
        """Test get_config with empty settings."""

        config = get_config()

        self.assertEqual(config["base_url"], "")
        self.assertEqual(config["listing_exclude"], [])
        self.assertIsInstance(config["listing_pages_config"], list)
        self.assertEqual(config["apps_exclude"], [])

        app_listing = config["listing_pages_config"]
        listing_pages_config = LISTING_PAGES_CONFIG
        self.assertEqual(len(app_listing), len(listing_pages_config))

    @override_settings(
        EXPOSAPI_CONFIG={
            "base_url": "https://example.com",
            "listing_exclude": ["listing_name"],
            "listing_pages_config": [
                {
                    "title": "Title",
                    "app_name": "app_name",
                    "listing_name": "listing_name",
                }
            ],
            "apps_exclude": ["app_name"],
        }
    )
    def test_get_config(self):
        """Test get_config with settings set."""

        config = get_config()

        self.assertEqual(config["base_url"], "https://example.com")
        self.assertEqual(config["listing_exclude"], ["listing_name"])
        self.assertEqual(
            config["listing_pages_config"],
            [
                {
                    "title": "Title",
                    "app_name": "app_name",
                    "listing_name": "listing_name",
                }
            ],
        )
        self.assertEqual(config["apps_exclude"], ["app_name"])

    def test_get_wagtail_core_listing_pages_config_default(self):
        """Test get_wagtail_core_listing_pages_config with default settings, where EXPOSAPI_CONFIG is not set."""

        config = get_wagtail_core_listing_pages_config()

        self.assertIsInstance(config, dict)
        self.assertEqual(config["title"], "Wagtail core listing pages")
        self.assertIsInstance(config["apps"], list)
        self.assertTrue(len(config["apps"]) > 0)

    @override_settings(
        EXPOSAPI_CONFIG={
            "base_url": "https://example.com",
            "listing_exclude": ["listing_name"],
            "listing_pages_config": [
                {
                    "title": "Title",
                    "app_name": "app_name",
                    "listing_name": "listing_name",
                }
            ],
            "apps_exclude": ["app_name"],
        }
    )
    def test_get_wagtail_core_listing_pages_config_exclude(self):
        """Test get_wagtail_core_listing_pages_config with settings set, where listing_exclude is set."""

        config = get_wagtail_core_listing_pages_config()

        self.assertIsInstance(config, dict)
        self.assertEqual(config["title"], "Wagtail core listing pages")
        self.assertIsInstance(config["apps"], list)
        self.assertEqual(len(config["apps"]), 0)
