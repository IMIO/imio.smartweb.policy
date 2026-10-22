# -*- coding: utf-8 -*-

from collective.messagesviewlet.utils import add_message
from collective.timedevents.events import IntervalTicks15Event
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from imio.smartweb.policy.caching import _LAST_MESSAGES_TICK
from imio.smartweb.policy.testing import IMIO_SMARTWEB_POLICY_FUNCTIONAL_TESTING
from plone import api
from plone.app.caching.operations.utils import getETag
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.event import notify

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

    def _page_etag_after_tick(self, **dates):
        """Return the page ETag before and after a tick, for an activated
        message with the given dates, the last tick being 10 minutes ago"""
        page = api.content.create(
            container=self.portal, type="imio.smartweb.Folder", id="folder"
        )
        message = add_message(
            id="message", title="Message", text="Road works", activate=True
        )
        for name, value in dates.items():
            setattr(message, name, value)
        message.reindexObject()
        keys = self._etags("moderateCaching")
        etag = getETag(page, self.request, keys=keys)
        now = datetime.now(timezone.utc)
        setattr(getUtility(IRegistry), _LAST_MESSAGES_TICK, now - timedelta(minutes=10))
        notify(IntervalTicks15Event(self.portal))
        return etag, getETag(page, self.request, keys=keys)

    def test_message_end_reached_changes_page_etag(self):
        now = datetime.now(timezone.utc)
        before, after = self._page_etag_after_tick(
            start=now - timedelta(days=1), end=now - timedelta(minutes=5)
        )
        self.assertNotEqual(after, before)

    def test_message_start_reached_changes_page_etag(self):
        now = datetime.now(timezone.utc)
        before, after = self._page_etag_after_tick(start=now - timedelta(minutes=5))
        self.assertNotEqual(after, before)

    def test_message_dates_not_reached_keep_page_etag(self):
        now = datetime.now(timezone.utc)
        before, after = self._page_etag_after_tick(
            start=now - timedelta(days=1), end=now + timedelta(days=1)
        )
        self.assertEqual(after, before)
