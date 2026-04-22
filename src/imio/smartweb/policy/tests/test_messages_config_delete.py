# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from imio.smartweb.policy.subscribers import prevent_messages_config_delete
from imio.smartweb.policy.testing import IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestMessagesConfigDeleteProtection(unittest.TestCase):
    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.messages_config = self.portal["messages-config"]

    def test_messages_config_workflow_limits_delete_objects_to_manager(self):
        workflow = self.portal.portal_workflow["messagesconfig_workflow"]
        state = workflow.states["private"]

        self.assertEqual(
            state.permission_roles["Delete objects"],
            ("Manager",),
        )

    def test_non_manager_cannot_delete_messages_config(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])

        with self.assertRaises(Unauthorized):
            self.portal.manage_delObjects(["messages-config"])

        self.assertIn("messages-config", self.portal.objectIds())

    def test_manager_can_delete_messages_config(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.portal.manage_delObjects(["messages-config"])

        self.assertNotIn("messages-config", self.portal.objectIds())

    def test_handler_blocks_non_manager(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])

        with self.assertRaises(Unauthorized):
            prevent_messages_config_delete(self.messages_config, None)

    def test_other_content_types_are_not_restricted(self):
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])

        prevent_messages_config_delete(self.portal, None)
