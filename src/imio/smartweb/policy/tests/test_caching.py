# -*- coding: utf-8 -*-

from collective.messagesviewlet.utils import add_message
from imio.smartweb.policy.testing import IMIO_SMARTWEB_POLICY_FUNCTIONAL_TESTING
from plone import api
from plone.app.caching.operations.utils import getETag
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest

OPERATIONS = ("moderateCaching", "terseCaching", "weakCaching")


class TestCaching(unittest.TestCase):
    layer = IMIO_SMARTWEB_POLICY_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _etags(self, operation):
        return api.portal.get_registry_record(f"plone.app.caching.{operation}.etags")

    def test_last_ban_in_etags(self):
        for operation in OPERATIONS:
            self.assertIn("lastBan", self._etags(operation))

    def test_upgrade_1044_to_1045_adds_last_ban(self):
        for operation in OPERATIONS:
            api.portal.set_registry_record(
                f"plone.app.caching.{operation}.etags",
                ("lastModified", "userid", "roles", "resourceRegistries"),
            )
        api.portal.get_tool("portal_setup").runAllImportStepsFromProfile(
            "profile-imio.smartweb.policy.upgrades:upgrade_1044_to_1045"
        )
        for operation in OPERATIONS:
            self.assertIn("lastBan", self._etags(operation))

    def test_message_changes_page_etag(self):
        page = api.content.create(
            container=self.portal, type="imio.smartweb.Folder", id="folder"
        )
        keys = self._etags("moderateCaching")
        etag = getETag(page, self.request, keys=keys)
        add_message(id="message", title="Message", text="Road works")
        self.assertNotEqual(getETag(page, self.request, keys=keys), etag)
