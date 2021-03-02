# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that imio.smartweb.policy is properly installed."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if imio.smartweb.policy is installed."""
        self.assertTrue(self.installer.isProductInstalled("imio.smartweb.policy"))

    def test_browserlayer(self):
        """Test that IImioSmartwebPolicyLayer is registered."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from plone.browserlayer import utils

        self.assertIn(IImioSmartwebPolicyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["imio.smartweb.policy"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.smartweb.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("imio.smartweb.policy"))

    def test_browserlayer_removed(self):
        """Test that IImioSmartwebPolicyLayer is removed."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from plone.browserlayer import utils

        self.assertNotIn(IImioSmartwebPolicyLayer, utils.registered_layers())
