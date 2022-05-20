# -*- coding: utf-8 -*-

from imio.smartweb.common.caching import ban_physicalpath
from plone import api
from plone.app.caching.operations.default import ModerateCaching
from plone.app.caching.operations.default import StrongCaching
from plone.app.caching.operations.default import TerseCaching
from plone.app.caching.operations.default import WeakCaching
from plone.caching.interfaces import ICachingOperationType
from plone.caching.utils import lookupOptions
from Products.CMFPlone.utils import parent
from zope.interface import provider

import logging

logger = logging.getLogger("imio.smartweb.policy")


def ban_for_message(obj, event):
    request = event.object.REQUEST
    portal = api.portal.get()
    physical_path = portal.getPhysicalPath()
    container = parent(obj)
    if container.portal_type != "MessagesConfig":
        # we are on a local message, ban only its container path
        physical_path = container.getPhysicalPath()
    ban_physicalpath(request, physical_path)


class PatchedCachingMixin:
    def interceptResponse(self, rulename, response, class_=None):
        result = super(PatchedCachingMixin, self).interceptResponse(
            rulename, response, class_
        )
        if result != "":
            # "" is the result of a 304 NOT MODIFIED
            return result

        options = lookupOptions(class_ or self.__class__, rulename)
        maxage = options.get("maxage", self.maxage)
        smaxage = options.get("smaxage", self.smaxage)

        if maxage:
            if smaxage is not None:
                maxage = f"{maxage}, s-maxage={smaxage}"
            response.setHeader(
                "Cache-Control",
                f"max-age={maxage}, proxy-revalidate, public",
            )
        elif smaxage:
            response.setHeader(
                "Cache-Control",
                f"max-age=0, s-maxage={smaxage}, must-revalidate",
            )
        else:
            response.setHeader("Cache-Control", "max-age=0, must-revalidate, private")

        return ""


@provider(ICachingOperationType)
class PatchedModerateCaching(PatchedCachingMixin, ModerateCaching):
    """Moderate caching with Cache-Control heaader set, even for 304"""


@provider(ICachingOperationType)
class PatchedStrongCaching(PatchedCachingMixin, StrongCaching):
    """Strong caching with Cache-Control heaader set, even for 304"""


@provider(ICachingOperationType)
class PatchedTerseCaching(PatchedCachingMixin, TerseCaching):
    """Terse caching with Cache-Control heaader set, even for 304"""


@provider(ICachingOperationType)
class PatchedWeakCaching(PatchedCachingMixin, WeakCaching):
    """Weak caching with Cache-Control heaader set, even for 304"""
