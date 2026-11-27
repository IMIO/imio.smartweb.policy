# -*- coding: utf-8 -*-
"""Setup tests for this package."""

from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest

ASSISTANT_ENABLED = (
    "imio.omnia.assistant.browser.controlpanel.IOmniaAssistantSettings.enabled"
)


class TestSetup(unittest.TestCase):
    """Test that imio.smartweb.policy is properly installed."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_profile_installed(self):
        """Test if imio.smartweb.policy:testing profile is installed."""
        self.assertTrue(
            self.installer.is_profile_installed("imio.smartweb.policy:testing")
        )

    def test_browserlayer(self):
        """Test that IImioSmartwebPolicyLayer is registered."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from plone.browserlayer import utils

        self.assertIn(IImioSmartwebPolicyLayer, utils.registered_layers())

    def test_upgrade_forgets_imio_prometheus(self):
        from imio.smartweb.policy.upgrades.upgrades import forget_imio_prometheus

        portal_setup = api.portal.get_tool("portal_setup")
        portal_setup.setLastVersionForProfile("imio.prometheus:default", "1000")
        forget_imio_prometheus(portal_setup)
        self.assertEqual(
            portal_setup.getLastVersionForProfile("imio.prometheus:default"), "unknown"
        )
        # Sites that never installed it: nothing to forget, no error
        forget_imio_prometheus(portal_setup)

    def test_upgrade_installs_omnia_assistant_turned_off(self):
        from imio.smartweb.policy.upgrades.upgrades import install_omnia_assistant

        portal_setup = api.portal.get_tool("portal_setup")
        install_omnia_assistant(portal_setup)
        self.assertTrue(self.installer.is_product_installed("imio.omnia.assistant"))
        self.assertFalse(api.portal.get_registry_record(ASSISTANT_ENABLED))

    def test_upgrade_keeps_the_settings_of_an_installed_assistant(self):
        from imio.smartweb.policy.upgrades.upgrades import install_omnia_assistant

        portal_setup = api.portal.get_tool("portal_setup")
        install_omnia_assistant(portal_setup)
        api.portal.set_registry_record(ASSISTANT_ENABLED, True)
        install_omnia_assistant(portal_setup)
        self.assertTrue(api.portal.get_registry_record(ASSISTANT_ENABLED))


class TestUninstall(unittest.TestCase):
    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("imio.smartweb.policy")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.smartweb.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("imio.smartweb.policy"))

    def test_browserlayer_removed(self):
        """Test that IImioSmartwebPolicyLayer is removed."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from plone.browserlayer import utils

        self.assertNotIn(IImioSmartwebPolicyLayer, utils.registered_layers())
