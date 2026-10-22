# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from imio.smartweb.common.caching import ban_physicalpath
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import parent
from zope.component import getUtility
from zope.globalrequest import getRequest

# Registry attribute holding the time of the last messages dates check
_LAST_MESSAGES_TICK = "__IMIO_SMARTWEB_LAST_MESSAGES_TICK"


def message_physicalpath(message):
    container = parent(message)
    if container.portal_type != "MessagesConfig":
        # we are on a local message, ban only its container path
        return container.getPhysicalPath()
    return api.portal.get().getPhysicalPath()


def ban_for_message(obj, event):
    request = event.object.REQUEST
    ban_physicalpath(request, message_physicalpath(obj))


def ban_for_message_dates(event):
    """A message appears / disappears when its start / end date is reached,
    without any event: ban the pages of the messages whose start or end date
    was reached since the last tick
    """
    registry = getUtility(IRegistry)
    now = datetime.now(timezone.utc)
    last_tick = getattr(registry, _LAST_MESSAGES_TICK, now - timedelta(minutes=15))
    setattr(registry, _LAST_MESSAGES_TICK, now)
    catalog = api.portal.get_tool("portal_catalog")
    dates = {"query": (last_tick, now), "range": "min:max"}
    physical_paths = set()
    for index in ("start", "end"):
        brains = catalog.unrestrictedSearchResults(
            portal_type="Message", review_state="activated", **{index: dates}
        )
        for brain in brains:
            message = brain._unrestrictedGetObject()
            physical_paths.add(message_physicalpath(message))
    for physical_path in physical_paths:
        ban_physicalpath(getRequest(), physical_path)
