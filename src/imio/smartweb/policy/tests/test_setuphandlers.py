# -*- coding: utf-8 -*-
"""Tests for setuphandlers.py module."""
from imio.smartweb.policy.setuphandlers import HiddenProfiles
from imio.smartweb.policy.setuphandlers import post_install
from imio.smartweb.policy.setuphandlers import register_cookie_policy
from imio.smartweb.policy.setuphandlers import register_gdpr_text
from imio.smartweb.policy.setuphandlers import setup_multilingual
from imio.smartweb.policy.setuphandlers import uninstall
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)
from plone import api
from plone.app.multilingual.interfaces import ILanguageRootFolder
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from unittest.mock import MagicMock
from unittest.mock import patch
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class TestHiddenProfiles(unittest.TestCase):
    """Test HiddenProfiles utility."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def test_hidden_profiles_implements_interface(self):
        """Test that HiddenProfiles implements INonInstallable."""
        from Products.CMFPlone.interfaces import INonInstallable

        hidden = HiddenProfiles()
        self.assertTrue(INonInstallable.providedBy(hidden))

    def test_get_non_installable_profiles(self):
        """Test getNonInstallableProfiles returns expected list."""
        hidden = HiddenProfiles()
        profiles = hidden.getNonInstallableProfiles()
        self.assertIsInstance(profiles, list)
        self.assertIn("imio.smartweb.common:default", profiles)
        self.assertIn("imio.smartweb.core:default", profiles)
        self.assertIn("imio.smartweb.policy:uninstall", profiles)
        self.assertIn("plone.app.multilingual:default", profiles)

    def test_get_non_installable_products(self):
        """Test getNonInstallableProducts returns expected list."""
        hidden = HiddenProfiles()
        products = hidden.getNonInstallableProducts()
        self.assertIsInstance(products, list)
        self.assertIn("imio.smartweb.common", products)
        self.assertIn("imio.smartweb.core", products)
        self.assertIn("imio.smartweb.policy.upgrades", products)
        self.assertIn("plone.app.multilingual", products)

    def test_hidden_profiles_registered_as_utility(self):
        """Test that HiddenProfiles is registered as a named utility."""
        from Products.CMFPlone.interfaces import INonInstallable

        hidden = getUtility(
            INonInstallable, name="imio.smartweb.policy-hiddenprofiles"
        )
        self.assertIsInstance(hidden, HiddenProfiles)


class TestPostInstall(unittest.TestCase):
    """Test post_install handler."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("imio.smartweb.policy.setuphandlers.remove_unused_contents")
    @patch("imio.smartweb.policy.setuphandlers.clear_manager_portlets")
    @patch("imio.smartweb.policy.setuphandlers.add_navigation_links")
    @patch("imio.smartweb.policy.setuphandlers.register_cookie_policy")
    @patch("imio.smartweb.policy.setuphandlers.register_gdpr_text")
    @patch("imio.smartweb.policy.setuphandlers.api.portal.get")
    def test_post_install_calls_all_setup_functions(
        self,
        mock_get_portal,
        mock_gdpr,
        mock_cookie,
        mock_nav,
        mock_clear,
        mock_remove,
    ):
        """Test post_install calls all expected setup functions."""
        mock_portal = MagicMock()
        mock_get_portal.return_value = mock_portal

        post_install(None)

        mock_get_portal.assert_called_once()
        mock_remove.assert_called_once_with(mock_portal)
        # clear_manager_portlets should be called 3 times
        self.assertEqual(mock_clear.call_count, 3)
        mock_clear.assert_any_call(mock_portal, "plone.leftcolumn")
        mock_clear.assert_any_call(mock_portal, "plone.rightcolumn")
        mock_clear.assert_any_call(mock_portal, "plone.footerportlets")
        mock_nav.assert_called_once_with(mock_portal)
        mock_cookie.assert_called_once_with(mock_portal)
        mock_gdpr.assert_called_once_with(mock_portal)


class TestRegisterCookiePolicy(unittest.TestCase):
    """Test register_cookie_policy function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_register_cookie_policy_sets_registry_record(self):
        """Test that register_cookie_policy sets the correct registry record."""
        register_cookie_policy(self.portal)

        cookie_text = api.portal.get_registry_record(
            "imio.gdpr.interfaces.IGDPRSettings.cookies_text"
        )
        self.assertIsNotNone(cookie_text)
        self.assertIn("Politique d'utilisation des cookies", cookie_text)
        self.assertIn("cookies essentiels", cookie_text)
        self.assertIn("cookies fonctionnels", cookie_text)

    def test_register_cookie_policy_with_none_portal(self):
        """Test that register_cookie_policy works when portal is None."""
        # Should not raise an exception
        register_cookie_policy(None)


class TestRegisterGdprText(unittest.TestCase):
    """Test register_gdpr_text function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_register_gdpr_text_sets_registry_record(self):
        """Test that register_gdpr_text sets the correct registry record."""
        with patch.dict("os.environ", {"WEBSITE_HOSTNAME": "Test Commune"}):
            register_gdpr_text(self.portal)

        gdpr_text = api.portal.get_registry_record(
            "imio.gdpr.interfaces.IGDPRSettings.text"
        )
        self.assertIsNotNone(gdpr_text)
        self.assertIn("Déclaration relative à la protection des données", gdpr_text)
        self.assertIn("Test Commune", gdpr_text)
        self.assertIn("RGPD", gdpr_text)

    def test_register_gdpr_text_without_hostname(self):
        """Test register_gdpr_text when WEBSITE_HOSTNAME is not set."""
        with patch.dict("os.environ", {}, clear=True):
            register_gdpr_text(self.portal)

        gdpr_text = api.portal.get_registry_record(
            "imio.gdpr.interfaces.IGDPRSettings.text"
        )
        self.assertIn("[nom du pouvoir local]", gdpr_text)


class TestSetupMultilingual(unittest.TestCase):
    """Test setup_multilingual function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_setup_multilingual_raises_error_with_single_language(self):
        """Test that setup_multilingual raises ValueError with only one language."""
        api.portal.set_registry_record("plone.available_languages", ["fr"])

        with self.assertRaises(ValueError) as cm:
            setup_multilingual(None)

        self.assertIn(
            "You should configure at least 2 languages", str(cm.exception)
        )

    @patch("imio.smartweb.policy.setuphandlers.add_navigation_links")
    def test_setup_multilingual_with_multiple_languages(self, mock_nav_links):
        """Test setup_multilingual with multiple languages configured."""
        # Set up multiple languages
        api.portal.set_registry_record("plone.available_languages", ["fr", "nl"])
        api.portal.set_registry_record("plone.default_language", "fr")

        # Create a test content item
        test_doc = api.content.create(
            container=self.portal, type="Document", id="test-doc", title="Test Document"
        )

        setup_multilingual(None)

        # Verify Language Root Folders were created
        self.assertTrue(hasattr(self.portal, "fr"))
        self.assertTrue(hasattr(self.portal, "nl"))

        fr_folder = getattr(self.portal, "fr")
        nl_folder = getattr(self.portal, "nl")

        self.assertTrue(ILanguageRootFolder.providedBy(fr_folder))
        self.assertTrue(ILanguageRootFolder.providedBy(nl_folder))

        # Verify content was moved to default language folder
        self.assertIn("test-doc", fr_folder.objectIds())

        # Verify add_navigation_links was called for non-default language
        mock_nav_links.assert_called_once_with(nl_folder, "nl")

    @patch("imio.smartweb.policy.setuphandlers.add_navigation_links")
    def test_setup_multilingual_preserves_default_page(self, mock_nav_links):
        """Test that setup_multilingual preserves the default page."""
        # Set up multiple languages
        api.portal.set_registry_record("plone.available_languages", ["fr", "nl"])
        api.portal.set_registry_record("plone.default_language", "fr")

        # Create a default page
        front_page = api.content.create(
            container=self.portal,
            type="Document",
            id="front-page",
            title="Front Page",
        )
        self.portal.setDefaultPage("front-page")

        setup_multilingual(None)

        # Verify default page is preserved in LRF
        fr_folder = getattr(self.portal, "fr")
        self.assertEqual(fr_folder.getDefaultPage(), "front-page")


class TestUninstall(unittest.TestCase):
    """Test uninstall handler."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def test_uninstall_does_not_raise_exception(self):
        """Test that uninstall handler completes without error."""
        # This is a placeholder test for the empty uninstall function
        try:
            uninstall(None)
        except Exception as e:
            self.fail(f"uninstall raised an exception: {e}")