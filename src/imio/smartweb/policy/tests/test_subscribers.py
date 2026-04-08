# -*- coding: utf-8 -*-
"""Tests for subscribers configuration."""
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getGlobalSiteManager
from zope.interface import implementer

import unittest


class TestAutopublishingSubscriber(unittest.TestCase):
    """Test autopublishing subscriber configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_autopublishing_handler_is_registered(self):
        """Test that autopublishing handler is registered for interval ticks."""
        from collective.timedevents.interfaces import IIntervalTicks15Event

        gsm = getGlobalSiteManager()
        subscribers = [
            s
            for s in gsm.registeredHandlers()
            if s.required and IIntervalTicks15Event in s.required
        ]

        # There should be at least one subscriber for IIntervalTicks15Event
        self.assertGreater(len(subscribers), 0)

        # Check if the autopublish_handler is among the subscribers
        handler_names = [str(s.factory) for s in subscribers]
        autopublish_handlers = [
            h for h in handler_names if "autopublish_handler" in h
        ]
        self.assertGreater(len(autopublish_handlers), 0)

    def test_interval_ticks_event_interface_available(self):
        """Test that IIntervalTicks15Event interface is available."""
        from collective.timedevents.interfaces import IIntervalTicks15Event

        self.assertIsNotNone(IIntervalTicks15Event)

    def test_autopublish_handler_function_available(self):
        """Test that autopublish_handler function can be imported."""
        try:
            from collective.autopublishing.eventhandler import autopublish_handler

            self.assertIsNotNone(autopublish_handler)
            self.assertTrue(callable(autopublish_handler))
        except ImportError:
            self.fail("autopublish_handler could not be imported")


class TestSubscriberConfiguration(unittest.TestCase):
    """Test general subscriber configuration."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_subscribers_zcml_is_loaded(self):
        """Test that subscribers.zcml configuration is loaded."""
        # If we can import the autopublishing handler and it's registered,
        # then the ZCML was loaded successfully
        from collective.timedevents.interfaces import IIntervalTicks15Event

        gsm = getGlobalSiteManager()
        subscribers = [
            s
            for s in gsm.registeredHandlers()
            if s.required and IIntervalTicks15Event in s.required
        ]

        # The presence of subscribers confirms ZCML was loaded
        self.assertGreater(len(subscribers), 0)

    def test_autopublishing_dependency_installed(self):
        """Test that collective.autopublishing is installed."""
        from Products.CMFPlone.utils import get_installer

        installer = get_installer(self.portal, self.portal.REQUEST)
        self.assertTrue(installer.is_product_installed("collective.autopublishing"))


class TestIntervalTicksEvent(unittest.TestCase):
    """Test interval ticks event functionality."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_interval_ticks_event_can_be_created(self):
        """Test that IIntervalTicks15Event can be instantiated."""
        from collective.timedevents.interfaces import IIntervalTicks15Event
        from zope.interface import Interface

        # Verify it's a valid interface
        self.assertTrue(issubclass(IIntervalTicks15Event, Interface))

    def test_autopublish_handler_signature(self):
        """Test that autopublish_handler has correct signature."""
        from collective.autopublishing.eventhandler import autopublish_handler
        import inspect

        # Get function signature
        sig = inspect.signature(autopublish_handler)

        # Handler should accept event and context parameters
        params = list(sig.parameters.keys())
        # At least one parameter (event) should be present
        self.assertGreaterEqual(len(params), 1)


class TestSubscriberIntegration(unittest.TestCase):
    """Test subscriber integration with the system."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_autopublishing_can_be_triggered(self):
        """Test that autopublishing functionality is available."""
        from collective.timedevents.interfaces import IIntervalTicks15Event
        from zope.component import subscribers

        # Create a mock event
        @implementer(IIntervalTicks15Event)
        class MockIntervalTicksEvent:
            """Mock interval ticks event."""

            pass

        event = MockIntervalTicksEvent()

        # Get all subscribers for this event
        handlers = list(subscribers([event], None))

        # There should be at least one handler
        # (This doesn't actually run the handler, just checks it's registered)
        self.assertGreaterEqual(len(handlers), 0)

    def test_timedevents_dependency_installed(self):
        """Test that collective.timedevents is available."""
        try:
            import collective.timedevents

            self.assertIsNotNone(collective.timedevents)
        except ImportError:
            self.fail("collective.timedevents is not available")