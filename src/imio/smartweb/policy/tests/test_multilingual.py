# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from imio.smartweb.policy.testing import IMIO_SMARTWEB_POLICY_FUNCTIONAL_TESTING
from plone import api
from plone.app.content.browser.contents.delete import DeleteActionView
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import transaction
import unittest


class TestMultilingual(unittest.TestCase):
    layer = IMIO_SMARTWEB_POLICY_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.portal.set_registry_record("plone.available_languages", ["fr", "en"])
        api.portal.set_registry_record("plone.default_language", "fr")
        applyProfile(self.portal, "imio.smartweb.policy:multilingual")
        transaction.commit()

    def test_site_administrator_cannot_delete_lrf(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        with self.assertRaises(Unauthorized):
            api.content.delete(self.portal.en, check_linkintegrity=False)
        self.assertIn("en", self.portal.objectIds())

    def test_site_administrator_cannot_delete_lrf_from_folder_contents(self):
        folder = api.content.create(
            container=self.portal.en, type="imio.smartweb.Folder", title="Folder"
        )
        transaction.commit()
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        view = DeleteActionView(self.portal, self.layer["request"])
        view.errors = []
        view.dest = self.portal
        view.action(self.portal.en)
        self.assertEqual(len(view.errors), 1)
        # folder_contents swallows Unauthorized: the publisher must abort
        self.assertTrue(transaction.get().isDoomed())
        transaction.abort()
        self.assertIn("en", self.portal.objectIds())
        catalog = api.portal.get_tool("portal_catalog")
        self.assertEqual(len(catalog(UID=api.content.get_uuid(self.portal.en))), 1)
        self.assertEqual(len(catalog(UID=api.content.get_uuid(folder))), 1)

    def test_site_administrator_can_delete_lrf_content(self):
        folder = api.content.create(
            container=self.portal.en, type="imio.smartweb.Folder", title="Folder"
        )
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        api.content.delete(folder, check_linkintegrity=False)
        self.assertNotIn("folder", self.portal.en.objectIds())

    def test_manager_can_delete_lrf(self):
        api.content.delete(self.portal.en, check_linkintegrity=False)
        self.assertNotIn("en", self.portal.objectIds())
