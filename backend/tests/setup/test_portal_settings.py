"""Portal settings tests."""

from plone import api

import pytest


class TestPortalSettings:
    """Test that Portal configuration is correctly done."""

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["plone.site_title", "Intranet da V2Tec"],
            ["plone.email_from_name", "Intranet da V2Tec"],
            ["plone.smtp_host", "localhost"],
            ["plone.smtp_port", 25],
            ["plone.navigation_depth", 4],
            ["plone.portal_timezone", "America/Sao_Paulo"],
            ["plone.available_timezones", ["America/Sao_Paulo"]],
            ["plone.twitter_username", "v2tec"],
            ["plone.default_language", "pt-br"],
            ["plone.available_languages", ["pt-br"]],
        ],
    )
    def test_setting(self, portal, key: str, expected: str | int):
        """Test registry setting."""
        value = api.portal.get_registry_record(key)
        assert value == expected
