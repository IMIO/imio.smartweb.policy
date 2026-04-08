# -*- coding: utf-8 -*-
"""Tests for permissions and roles configuration."""
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

import unittest


class TestPermissionsConfiguration(unittest.TestCase):
    """Test permissions configuration from rolemap.xml."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_portlets_manage_permission_not_acquired(self):
        """Test that Portlets: Manage portlets permission is not acquired."""
        permission = "Portlets: Manage portlets"
        # Get permission settings for the portal
        permission_settings = self.portal.permission_settings(permission)
        # The acquire setting should be False (0)
        self.assertEqual(permission_settings[0]["acquire"], "")

    def test_plone_site_setup_site_permission_manager_only(self):
        """Test that Plone Site Setup: Site is Manager only."""
        permission = "Plone Site Setup: Site"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_plone_site_setup_security_permission_manager_only(self):
        """Test that Plone Site Setup: Security is Manager only."""
        permission = "Plone Site Setup: Security"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_plone_site_setup_types_permission_manager_only(self):
        """Test that Plone Site Setup: Types is Manager only."""
        permission = "Plone Site Setup: Types"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_content_rules_manage_rules_permission_manager_only(self):
        """Test that Content rules: Manage rules is Manager only."""
        permission = "Content rules: Manage rules"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)


class TestCustomPermissions(unittest.TestCase):
    """Test custom Smartweb permissions."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_smartweb_manager_only_configlets_permission_exists(self):
        """Test that Smartweb: Manager-only configlets permission exists."""
        permission = "Smartweb: Manager-only configlets"
        all_permissions = [p["name"] for p in self.portal.permissionsOfRole("Manager")]
        self.assertIn(permission, all_permissions)

    def test_smartweb_manager_only_configlets_manager_role(self):
        """Test that Manager has Smartweb: Manager-only configlets permission."""
        permission = "Smartweb: Manager-only configlets"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)

    def test_smartweb_manager_only_configlets_not_site_admin(self):
        """Test that Site Administrator doesn't have Manager-only configlets permission."""
        permission = "Smartweb: Manager-only configlets"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertNotIn("Site Administrator", roles)

    def test_smartweb_manage_configlets_permission_exists(self):
        """Test that Smartweb: Manage configlets permission exists."""
        permission = "Smartweb: Manage configlets"
        all_permissions = [p["name"] for p in self.portal.permissionsOfRole("Manager")]
        self.assertIn(permission, all_permissions)

    def test_smartweb_manage_configlets_manager_role(self):
        """Test that Manager has Smartweb: Manage configlets permission."""
        permission = "Smartweb: Manage configlets"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)

    def test_smartweb_manage_configlets_site_admin_role(self):
        """Test that Site Administrator has Smartweb: Manage configlets permission."""
        permission = "Smartweb: Manage configlets"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Site Administrator", roles)


class TestSiteSetupPermissions(unittest.TestCase):
    """Test various site setup permissions."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_mail_permission_manager_only(self):
        """Test that Plone Site Setup: Mail is Manager only."""
        permission = "Plone Site Setup: Mail"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_language_permission_manager_only(self):
        """Test that Plone Site Setup: Language is Manager only."""
        permission = "Plone Site Setup: Language"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_navigation_permission_manager_only(self):
        """Test that Plone Site Setup: Navigation is Manager only."""
        permission = "Plone Site Setup: Navigation"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_search_permission_manager_only(self):
        """Test that Plone Site Setup: Search is Manager only."""
        permission = "Plone Site Setup: Search"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_themes_permission_manager_only(self):
        """Test that Plone Site Setup: Themes is Manager only."""
        permission = "Plone Site Setup: Themes"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_tinymce_permission_manager_only(self):
        """Test that Plone Site Setup: TinyMCE is Manager only."""
        permission = "Plone Site Setup: TinyMCE"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_markup_permission_manager_only(self):
        """Test that Plone Site Setup: Markup is Manager only."""
        permission = "Plone Site Setup: Markup"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_editing_permission_manager_only(self):
        """Test that Plone Site Setup: Editing is Manager only."""
        permission = "Plone Site Setup: Editing"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_filtering_permission_manager_only(self):
        """Test that Plone Site Setup: Filtering is Manager only."""
        permission = "Plone Site Setup: Filtering"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)


class TestInspectRelationsPermission(unittest.TestCase):
    """Test Inspect Relations permission."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_inspect_relations_permission_manager_only(self):
        """Test that Inspect Relations permission is Manager only."""
        permission = "Inspect Relations"
        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]
        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)


class TestPermissionsNotAcquired(unittest.TestCase):
    """Test that certain permissions are not acquired."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_smartweb_permissions_not_acquired(self):
        """Test that custom Smartweb permissions are not acquired."""
        permissions = [
            "Smartweb: Manager-only configlets",
            "Smartweb: Manage configlets",
        ]

        for permission in permissions:
            permission_settings = self.portal.permission_settings(permission)
            # The acquire setting should be False (empty string when not acquired)
            self.assertEqual(permission_settings[0]["acquire"], "")

    def test_site_setup_permissions_not_acquired(self):
        """Test that site setup permissions are not acquired."""
        permissions = [
            "Plone Site Setup: Site",
            "Plone Site Setup: Mail",
            "Plone Site Setup: Security",
            "Plone Site Setup: Types",
        ]

        for permission in permissions:
            permission_settings = self.portal.permission_settings(permission)
            # The acquire setting should be False (empty string when not acquired)
            self.assertEqual(permission_settings[0]["acquire"], "")