# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as quiskinstallinterfaces
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "imio.smartweb.core:default",
            "imio.smartweb.policy:uninstall",
        ]


@implementer(quiskinstallinterfaces.INonInstallable)
class HiddenProducts(object):
    def getNonInstallableProducts(self):
        """Hides profiles from QuickInstaller"""
        return [
            u"imio.smartweb.core",
        ]


def post_install(context):
    """Post install script"""


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
