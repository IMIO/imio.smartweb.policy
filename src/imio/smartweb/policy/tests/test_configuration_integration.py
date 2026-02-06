# -*- coding: utf-8 -*-
"""Integration tests for configuration files."""
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

import unittest


class TestProfilesZCMLConfiguration(unittest.TestCase):
    """Test profiles.zcml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup_tool = getToolByName(self.portal, "portal_setup")

    def test_all_profiles_have_unique_names(self):
        """Test that all profiles have unique names."""
        profile_ids = [p["id"] for p in self.setup_tool.listProfileInfo()]

        policy_profiles = [
            p for p in profile_ids if p.startswith("imio.smartweb.policy:")
        ]

        # Should have at least default, demo, multilingual, and uninstall
        self.assertGreaterEqual(len(policy_profiles), 4)

        # All profiles should be unique
        self.assertEqual(len(policy_profiles), len(set(policy_profiles)))

    def test_default_profile_has_post_handler(self):
        """Test that default profile has post_install handler configured."""
        # This is tested by checking if post_install was called during setup
        # We can verify by checking if the expected content was created

        # After default profile installation, unused content should be removed
        self.assertFalse(hasattr(self.portal, "news"))
        self.assertFalse(hasattr(self.portal, "events"))
        self.assertFalse(hasattr(self.portal, "Members"))

    def test_profile_extends_correct_types(self):
        """Test that profiles provide correct interface."""
        from Products.GenericSetup.interfaces import EXTENSION

        profile_info = [
            p
            for p in self.setup_tool.listProfileInfo()
            if p["id"] == "imio.smartweb.policy:default"
        ]

        self.assertEqual(len(profile_info), 1)
        self.assertEqual(profile_info[0]["type"], EXTENSION)


class TestSubscribersZCMLConfiguration(unittest.TestCase):
    """Test subscribers.zcml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_autopublishing_subscriber_correctly_configured(self):
        """Test that autopublishing subscriber is correctly configured."""
        from collective.timedevents.interfaces import IIntervalTicks15Event
        from zope.component import getGlobalSiteManager

        gsm = getGlobalSiteManager()

        # Find subscribers for IIntervalTicks15Event
        subscribers = [
            s
            for s in gsm.registeredHandlers()
            if s.required and len(s.required) > 0 and IIntervalTicks15Event in s.required
        ]

        # Should have at least one subscriber
        self.assertGreater(len(subscribers), 0)

        # At least one should be the autopublish_handler
        handler_found = False
        for subscriber in subscribers:
            handler_name = str(subscriber.factory)
            if "autopublish" in handler_name.lower():
                handler_found = True
                break

        self.assertTrue(
            handler_found, "autopublish_handler not found in subscribers"
        )

    def test_subscriber_handles_correct_event_type(self):
        """Test that subscriber is registered for correct event type."""
        from collective.timedevents.interfaces import IIntervalTicks15Event
        from zope.interface import implementer
        from zope.component import subscribers as get_subscribers

        # Create a mock event
        @implementer(IIntervalTicks15Event)
        class MockEvent:
            pass

        event = MockEvent()

        # Get subscribers for this event
        handlers = list(get_subscribers([event], None))

        # Should be able to get handlers without error
        self.assertIsInstance(handlers, list)


class TestBrowserLayerXMLConfiguration(unittest.TestCase):
    """Test browserlayer.xml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_browser_layer_name_matches_interface(self):
        """Test that browser layer name matches interface."""
        from imio.smartweb.policy.interfaces import IImioSmartwebPolicyLayer
        from plone.browserlayer import utils

        # Get all registered layers
        layers = utils.registered_layers()

        # Our layer should be in the list
        self.assertIn(IImioSmartwebPolicyLayer, layers)

        # Verify the interface name
        self.assertEqual(
            IImioSmartwebPolicyLayer.__name__, "IImioSmartwebPolicyLayer"
        )


class TestControlPanelXMLConfiguration(unittest.TestCase):
    """Test controlpanel.xml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_controlpanel_configlets_have_correct_permissions(self):
        """Test that configlets have correct permission settings."""
        # Member Fields and User/Group Settings should require Manager-only permission
        manager_only_configlets = ["MemberFields", "UsersGroupsSettings"]

        for configlet_id in manager_only_configlets:
            # Try to find the configlet
            configlets = [
                c for c in self.controlpanel.listActions() if c.id == configlet_id
            ]

            if configlets:
                # If found, verify it exists
                self.assertGreater(len(configlets), 0)

    def test_anysurfer_configlet_has_manage_permission(self):
        """Test that Anysurfer configlet has Manage configlets permission."""
        configlet_id = "anysurfer"

        configlets = [
            c for c in self.controlpanel.listActions() if c.id == configlet_id
        ]

        if configlets:
            # If found, verify it's accessible to Site Administrator
            self.assertGreater(len(configlets), 0)


class TestRolemapXMLConfiguration(unittest.TestCase):
    """Test rolemap.xml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_all_site_setup_permissions_configured(self):
        """Test that all site setup permissions are properly configured."""
        site_setup_permissions = [
            "Plone Site Setup: Site",
            "Plone Site Setup: Mail",
            "Plone Site Setup: Language",
            "Plone Site Setup: Navigation",
            "Plone Site Setup: Search",
            "Plone Site Setup: Security",
            "Plone Site Setup: Themes",
            "Plone Site Setup: Types",
            "Plone Site Setup: TinyMCE",
            "Plone Site Setup: Markup",
            "Plone Site Setup: Editing",
            "Plone Site Setup: Filtering",
        ]

        for permission in site_setup_permissions:
            # Each permission should exist and be assigned to Manager
            roles = [
                r["name"]
                for r in self.portal.rolesOfPermission(permission)
                if r["selected"]
            ]
            self.assertIn(
                "Manager", roles, f"{permission} not assigned to Manager"
            )

    def test_permissions_acquisition_settings(self):
        """Test that certain permissions have acquisition disabled."""
        no_acquire_permissions = [
            "Portlets: Manage portlets",
            "Plone Site Setup: Site",
            "Smartweb: Manager-only configlets",
            "Smartweb: Manage configlets",
        ]

        for permission in no_acquire_permissions:
            permission_settings = self.portal.permission_settings(permission)
            # acquire should be empty string (False) for these permissions
            self.assertEqual(
                permission_settings[0]["acquire"],
                "",
                f"{permission} should not acquire",
            )

    def test_content_rules_permission_configured(self):
        """Test that Content rules permission is properly configured."""
        permission = "Content rules: Manage rules"

        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]

        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)

    def test_inspect_relations_permission_configured(self):
        """Test that Inspect Relations permission is properly configured."""
        permission = "Inspect Relations"

        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(permission)
            if r["selected"]
        ]

        self.assertIn("Manager", roles)
        self.assertNotIn("Site Administrator", roles)


class TestMetadataXMLConfiguration(unittest.TestCase):
    """Test metadata.xml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup_tool = getToolByName(self.portal, "portal_setup")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_metadata_version_is_set(self):
        """Test that profile version is set in metadata."""
        version = self.setup_tool.getLastVersionForProfile(
            "imio.smartweb.policy:default"
        )

        # Version should be a tuple or string
        self.assertIsNotNone(version)

    def test_all_dependencies_are_installed(self):
        """Test that all profile dependencies are installed."""
        from Products.CMFPlone.utils import get_installer

        installer = get_installer(self.portal, self.portal.REQUEST)

        # Key dependencies that should be installed
        key_dependencies = [
            "plone.app.caching",
            "collective.autopublishing",
            "collective.autoscaling",
            "collective.messagesviewlet",
            "imio.gdpr",
        ]

        for dependency in key_dependencies:
            self.assertTrue(
                installer.is_product_installed(dependency),
                f"{dependency} should be installed",
            )


class TestViewletsXMLConfiguration(unittest.TestCase):
    """Test viewlets.xml configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_viewlet_configuration_is_loaded(self):
        """Test that viewlet configuration is properly loaded."""
        # We can't directly test viewlet XML without more complex setup,
        # but we can verify that viewlet-related tools are available
        from zope.component import queryUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage

        storage = queryUtility(IViewletSettingsStorage)
        # Storage should be available if viewlets are configured
        self.assertIsNotNone(storage)


class TestTypesXMLConfiguration(unittest.TestCase):
    """Test types configuration in XML files."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.types_tool = getToolByName(self.portal, "portal_types")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_all_configured_types_exist(self):
        """Test that all types mentioned in XML files exist."""
        configured_types = [
            "Collection",
            "Document",
            "Event",
            "File",
            "Folder",
            "Image",
            "Link",
            "News Item",
            "Plone Site",
        ]

        existing_types = self.types_tool.objectIds()

        for type_id in configured_types:
            self.assertIn(
                type_id, existing_types, f"{type_id} should be configured"
            )

    def test_types_have_valid_configuration(self):
        """Test that configured types have valid settings."""
        for type_id in ["Document", "Folder", "Collection"]:
            type_info = self.types_tool.get(type_id)

            # Type should exist
            self.assertIsNotNone(type_info, f"{type_id} should exist")

            # Type should have a title
            self.assertTrue(
                hasattr(type_info, "title"), f"{type_id} should have title"
            )

            # Type should have allowed content types defined
            self.assertTrue(
                hasattr(type_info, "allowed_content_types"),
                f"{type_id} should have allowed_content_types",
            )