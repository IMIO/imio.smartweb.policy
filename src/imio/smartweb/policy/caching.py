# -*- coding: utf-8 -*-

from imio.smartweb.common.caching import ban_physicalpath
from plone import api
from Products.CMFPlone.utils import parent


def ban_for_message(obj, event):
    request = event.object.REQUEST
    portal = api.portal.get()
    physical_path = portal.getPhysicalPath()
    container = parent(obj)
    if container.portal_type != "MessagesConfig":
        # we are on a local message, ban only its container path
        physical_path = container.getPhysicalPath()
    ban_physicalpath(request, physical_path)
