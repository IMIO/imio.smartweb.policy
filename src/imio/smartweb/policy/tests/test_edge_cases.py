# -*- coding: utf-8 -*-
"""Edge case and regression tests for imio.smartweb.policy."""
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import patch

import unittest


class TestSetupHandlersEdgeCases(unittest.TestCase):
    """Test edge cases in setup handlers."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_register_gdpr_text_with_special_characters(self):
        """Test GDPR registration with special characters in commune name."""
        from imio.smartweb.policy.setuphandlers import register_gdpr_text

        special_commune = "Commune d'Été & Spécial <test>"
        with patch.dict("os.environ", {"WEBSITE_HOSTNAME": special_commune}):
            register_gdpr_text(self.portal)

        gdpr_text = api.portal.get_registry_record(
            "imio.gdpr.interfaces.IGDPRSettings.text"
        )
        # Verify the special characters are preserved
        self.assertIn("Commune d'Été & Spécial <test>", gdpr_text)

    def test_post_install_idempotency(self):
        """Test that running post_install multiple times doesn't cause errors."""
        from imio.smartweb.policy.setuphandlers import post_install

        # Run post_install multiple times
        try:
            post_install(None)
            post_install(None)
            post_install(None)
        except Exception as e:
            self.fail(f"post_install should be idempotent but raised: {e}")


class TestUtilsEdgeCases(unittest.TestCase):
    """Test edge cases in utility functions."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_remove_unused_contents_when_already_removed(self):
        """Test remove_unused_contents when folders don't exist."""
        from imio.smartweb.policy.utils import remove_unused_contents

        # Ensure folders don't exist
        if hasattr(self.portal, "news"):
            api.content.delete(self.portal.news)
        if hasattr(self.portal, "events"):
            api.content.delete(self.portal.events)
        if hasattr(self.portal, "Members"):
            api.content.delete(self.portal.Members)

        # Should not raise an error
        try:
            remove_unused_contents(self.portal)
        except Exception as e:
            self.fail(f"remove_unused_contents should handle missing folders: {e}")

    def test_clear_manager_portlets_with_no_portlets(self):
        """Test clearing portlets when none exist."""
        from imio.smartweb.policy.utils import clear_manager_portlets

        # This should not raise an error even if no portlets exist
        try:
            clear_manager_portlets(self.portal, "plone.leftcolumn")
        except Exception as e:
            self.fail(f"clear_manager_portlets should handle empty managers: {e}")

    @patch("imio.smartweb.policy.utils.get_vocabulary")
    def test_add_iam_folder_with_empty_vocabulary(self, mock_vocab):
        """Test add_iam_folder with empty vocabulary."""
        from imio.smartweb.policy.utils import add_iam_folder

        mock_vocab.return_value = []

        add_iam_folder(self.portal, "fr")

        # Verify folder was created even with empty vocabulary
        self.assertTrue(hasattr(self.portal, "i-am"))
        iam_folder = getattr(self.portal, "i-am")

        # Verify no links were created
        links = iam_folder.objectValues()
        self.assertEqual(len(links), 0)

    def test_get_gdpr_html_content_with_empty_commune(self):
        """Test get_gdpr_html_content with empty string commune."""
        from imio.smartweb.policy.utils import get_gdpr_html_content

        result = get_gdpr_html_content("")

        # Empty string should be treated as None
        self.assertIn("[nom du pouvoir local]", result)

    def test_get_ts_api_base_url_with_malformed_url(self):
        """Test get_ts_api_base_url with various malformed URLs."""
        from imio.smartweb.policy.utils import get_ts_api_base_url

        with patch("imio.smartweb.core.utils.get_value_from_registry") as mock_get:
            with patch("imio.smartweb.core.utils.is_valid_url") as mock_valid:
                # Test with None
                mock_get.return_value = None
                mock_valid.return_value = False
                result = get_ts_api_base_url()
                self.assertIsNone(result)


class TestMultilingualSetupEdgeCases(unittest.TestCase):
    """Test edge cases in multilingual setup."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_setup_multilingual_with_exactly_two_languages(self):
        """Test setup_multilingual with minimum required languages."""
        from imio.smartweb.policy.setuphandlers import setup_multilingual

        api.portal.set_registry_record("plone.available_languages", ["fr", "nl"])
        api.portal.set_registry_record("plone.default_language", "fr")

        # Should not raise an error
        try:
            setup_multilingual(None)
        except ValueError:
            self.fail("setup_multilingual should accept exactly 2 languages")

    def test_setup_multilingual_with_many_languages(self):
        """Test setup_multilingual with many languages."""
        from imio.smartweb.policy.setuphandlers import setup_multilingual

        languages = ["fr", "nl", "en", "de", "es"]
        api.portal.set_registry_record("plone.available_languages", languages)
        api.portal.set_registry_record("plone.default_language", "fr")

        # Should handle multiple languages
        try:
            setup_multilingual(None)
        except Exception as e:
            self.fail(f"setup_multilingual should handle many languages: {e}")


class TestPermissionsEdgeCases(unittest.TestCase):
    """Test edge cases in permissions configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_all_custom_permissions_are_defined(self):
        """Test that all custom Smartweb permissions are properly defined."""
        custom_permissions = [
            "Smartweb: Manager-only configlets",
            "Smartweb: Manage configlets",
        ]

        for permission in custom_permissions:
            # Should be able to get roles for this permission
            roles = self.portal.rolesOfPermission(permission)
            self.assertIsInstance(roles, list)
            self.assertGreater(len(roles), 0)

    def test_permission_settings_consistency(self):
        """Test that permission settings are consistent across roles."""
        permission = "Smartweb: Manager-only configlets"

        # Get roles with this permission
        roles_with_permission = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]

        # Manager should have it, Site Administrator should not
        self.assertIn("Manager", roles_with_permission)
        self.assertNotIn("Site Administrator", roles_with_permission)


class TestContentTypeEdgeCases(unittest.TestCase):
    """Test edge cases in content type configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_all_standard_types_are_available(self):
        """Test that all standard Plone content types are available."""
        from Products.CMFCore.utils import getToolByName

        types_tool = getToolByName(self.portal, "portal_types")

        standard_types = [
            "Document",
            "Event",
            "File",
            "Folder",
            "Image",
            "Link",
            "News Item",
            "Collection",
        ]

        for type_id in standard_types:
            self.assertIn(type_id, types_tool.objectIds())

    def test_content_types_are_addable(self):
        """Test that content types can actually be created."""
        # Create a test folder
        folder = api.content.create(
            container=self.portal,
            type="Folder",
            id="test-folder",
            title="Test Folder",
        )

        # Try to create different content types
        types_to_test = [
            ("Document", "test-document"),
            ("File", "test-file"),
            ("Image", "test-image"),
        ]

        for content_type, content_id in types_to_test:
            try:
                obj = api.content.create(
                    container=folder,
                    type=content_type,
                    id=content_id,
                    title=f"Test {content_type}",
                )
                self.assertIsNotNone(obj)
            except Exception as e:
                self.fail(
                    f"Failed to create {content_type}: {e}"
                )


class TestSubscribersEdgeCases(unittest.TestCase):
    """Test edge cases in subscriber configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_multiple_interval_ticks_handlers(self):
        """Test that multiple handlers can be registered for interval ticks."""
        from collective.timedevents.interfaces import IIntervalTicks15Event
        from zope.component import getGlobalSiteManager

        gsm = getGlobalSiteManager()
        subscribers = [
            s
            for s in gsm.registeredHandlers()
            if s.required and IIntervalTicks15Event in s.required
        ]

        # There should be at least one subscriber
        self.assertGreater(len(subscribers), 0)

        # Each subscriber should have a valid factory
        for subscriber in subscribers:
            self.assertIsNotNone(subscriber.factory)


class TestBrowserLayerEdgeCases(unittest.TestCase):
    """Test edge cases in browser layer configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_browser_layer_uniqueness(self):
        """Test that browser layer is unique and not duplicated."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from plone.browserlayer import utils

        layers = utils.registered_layers()

        # Count how many times our layer appears
        count = sum(1 for layer in layers if layer == IImioSmartwebPolicyLayer)

        # Should appear exactly once
        self.assertEqual(count, 1)

    def test_browser_layer_inheritance(self):
        """Test that browser layer properly inherits from Interface."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from zope.interface import Interface

        # Verify inheritance chain
        self.assertTrue(issubclass(IImioSmartwebPolicyLayer, Interface))