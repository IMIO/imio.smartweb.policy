# -*- coding: utf-8 -*-

from imio.smartweb.policy.utils import add_navigation_links
from imio.smartweb.policy.utils import clear_manager_portlets
from imio.smartweb.policy.utils import remove_unused_contents
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "imio.smartweb.common:default",
            "imio.smartweb.core:default",
            "imio.smartweb.policy:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide unwanted products from site-creation and quickinstaller."""
        return [
            "imio.smartweb.common",
            "imio.smartweb.core",
            "imio.smartweb.policy.upgrades",
        ]


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    remove_unused_contents(portal)
    clear_manager_portlets(portal, "plone.leftcolumn")
    clear_manager_portlets(portal, "plone.rightcolumn")
    clear_manager_portlets(portal, "plone.footerportlets")
    add_navigation_links(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
