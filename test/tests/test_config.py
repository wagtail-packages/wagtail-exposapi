from django.conf import settings as django_settings

import pytest

from exposapi.config import get_config, get_wagtail_core_listing_pages_config


class TestAutouseFixture:
    @pytest.fixture(autouse=True)
    def configure_settings(self, settings):
        # The `settings` argument is a fixture provided by pytest-django.
        settings.FOO = "bar"

    def test_one(self):
        assert django_settings.FOO == "bar"

    def test_two(self):
        assert django_settings.FOO == "bar"


class TestConfig:
    def test_get_config_default(self):
        """Test get_config with default settings, where EXPOSAPI_CONFIG is not set."""

        config = get_config()

        assert config["listing_exclude"] == []
        assert isinstance(config["listing_pages_config"], list)
        assert len(config["listing_pages_config"]) > 0
        assert config["listing_pages_config"][0]["title"] == "Search promotions"
        assert config["listing_pages_config"][-1]["title"] == "Groups"
        assert config["apps_exclude"] == []

    def test_get_config_custom(self, settings):
        """Test get_config with custom settings, where EXPOSAPI_CONFIG is set.
        But no data has been added to the values."""

        settings.EXPOSAPI_CONFIG = {
            "listing_exclude": [],
            "listing_pages_config": [],
            "apps_exclude": [],
        }

        config = get_config()

        assert config["listing_exclude"] == []
        assert isinstance(config["listing_pages_config"], list)
        assert len(config["listing_pages_config"]) > 0
        assert config["listing_pages_config"][0]["title"] == "Search promotions"
        assert config["listing_pages_config"][-1]["title"] == "Groups"
        assert config["apps_exclude"] == []

    def test_get_config_custom_with_data(self, settings):
        """Test get_config with custom settings, where EXPOSAPI_CONFIG is set.
        And data has been added to the values."""

        settings.EXPOSAPI_CONFIG = {
            "listing_exclude": ["wagtailusers_groups:index"],
            "listing_pages_config": [
                {
                    "title": "Search promotions",
                    "app_name": None,
                    "listing_name": "exposapi_search:index",
                },
                {
                    "title": "Groups",
                    "app_name": None,
                    "listing_name": "wagtailusers_groups:index",
                },
            ],
            "apps_exclude": ["wagtailusers"],
        }

        config = get_config()

        assert config["listing_exclude"] == ["wagtailusers_groups:index"]
        assert isinstance(config["listing_pages_config"], list)
        assert len(config["listing_pages_config"]) > 0
        assert config["listing_pages_config"][0]["title"] == "Search promotions"
        assert config["listing_pages_config"][-1]["title"] == "Groups"
        assert config["apps_exclude"] == ["wagtailusers"]

    def test_get_wagtail_core_listing_pages_config_default(self):
        """Test get_wagtail_core_listing_pages_config with default settings, where EXPOSAPI_CONFIG is not set."""

        config = get_wagtail_core_listing_pages_config()

        assert config["title"] == "Wagtail core listing pages"
        assert isinstance(config["apps"], list)
        assert len(config["apps"]) > 0
        assert config["apps"][0]["title"] == "Search promotions"
        assert config["apps"][-1]["title"] == "Groups"

    def test_get_wagtail_core_listing_pages_config_custom(self, settings):
        """Test get_wagtail_core_listing_pages_config with custom settings, where EXPOSAPI_CONFIG is set.
        But no data has been added to the values."""

        settings.EXPOSAPI_CONFIG = {
            "listing_exclude": [],
            "listing_pages_config": [],
            "apps_exclude": [],
        }

        config = get_wagtail_core_listing_pages_config()

        assert config["title"] == "Wagtail core listing pages"
        assert isinstance(config["apps"], list)
        assert len(config["apps"]) > 0
        assert config["apps"][0]["title"] == "Search promotions"
        assert config["apps"][-1]["title"] == "Groups"

    def test_get_wagtail_core_listing_pages_config_list_exclude(self, settings):
        """Test get_wagtail_core_listing_pages_config with custom settings, where EXPOSAPI_CONFIG is set.
        Testing the listing_exclude value."""

        settings.EXPOSAPI_CONFIG = {
            "listing_exclude": ["wagtailusers_groups:index"],
            "listing_pages_config": [],
            "apps_exclude": [],
        }

        config = get_wagtail_core_listing_pages_config()

        assert config["title"] == "Wagtail core listing pages"
        assert isinstance(config["apps"], list)
        assert len(config["apps"]) > 0
        assert config["apps"][0]["title"] == "Search promotions"
        assert config["apps"][-1]["title"] == "Reports Workflows"

        assert len(config["apps"]) == len(get_config()["listing_pages_config"]) - 1
