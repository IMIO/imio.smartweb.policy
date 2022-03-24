# -*- coding: utf-8 -*-

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
import os
import requests

logger = logging.getLogger("imio.smartweb.policy")


def ban_for_message(obj, event):
    portal = api.portal.get()
    caching_server = os.environ.get("CACHING_SERVERS", "")
    forwarded_host = event.object.REQUEST.get("X-Forwarded-Host", "")
    headers = {"Host": forwarded_host}
    ban_url = caching_server
    container = parent(obj)
    if container.portal_type != "MessagesConfig":
        # we are on a local banner, ban only its container path
        len_portal_path = len(portal.getPhysicalPath())
        relative_path = "/".join(container.getPhysicalPath()[len_portal_path:])
        ban_url = f"{caching_server}/{relative_path}"
    logger.info(f"## X-Forwarded-Host : {forwarded_host} ## ban_url : {ban_url}")
    requests.request("BAN", ban_url, headers=headers)


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
