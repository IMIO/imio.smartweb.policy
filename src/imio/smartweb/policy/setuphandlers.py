# -*- coding: utf-8 -*-

from imio.smartweb.policy.utils import add_navigation_links
from imio.smartweb.policy.utils import clear_manager_portlets
from imio.smartweb.policy.utils import remove_unused_contents
from plone import api
from plone.app.multilingual.interfaces import ILanguageRootFolder
from plone.app.multilingual.subscriber import set_recursive_language
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces.constrains import DISABLED
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.interface import implementer

import logging

logger = logging.getLogger("imio.smartweb.policy")


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


def setup_multilingual(context):
    available_languages = api.portal.get_registry_record("plone.available_languages")
    if len(available_languages) < 2:
        raise ValueError("You should configure at least 2 languages for the site")

    portal = api.portal.get()
    default_page = getattr(portal, "default_page", None)

    # install plone.app.multilingual
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile("plone.app.multilingual:default")

    # move existing root contents to default lang LRF
    default_lang = api.portal.get_registry_record("plone.default_language")
    lrf = getattr(portal, default_lang)
    for obj in portal.listFolderContents():
        portal_type = obj.portal_type
        if ILanguageRootFolder.providedBy(obj):
            continue
        if portal_type == "MessagesConfig":
            # TODO: determine if we need one MessagesConfig folder by LRF
            continue
        set_recursive_language(obj, default_lang)
        if portal_type in ["imio.smartweb.HeroBanner", "imio.smartweb.Footer"]:
            # we need to temporarily authorize these content types in LRF
            container = ISelectableConstrainTypes(lrf)
            constrain_types_mode = container.getConstrainTypesMode()
            container.setConstrainTypesMode(DISABLED)
            pt = api.portal.get_tool("portal_types")
            allowed_content_types = pt.getTypeInfo("LRF").allowed_content_types
            allowed_content_types = list(allowed_content_types)
            allowed_content_types.append(portal_type)
            pt.getTypeInfo("LRF").allowed_content_types = tuple(allowed_content_types)
            api.content.move(obj, target=lrf)
            allowed_content_types.remove(portal_type)
            pt.getTypeInfo("LRF").allowed_content_types = tuple(allowed_content_types)
            container.setConstrainTypesMode(constrain_types_mode)
        else:
            api.content.move(obj, target=lrf)
        logger.info(f"Moved {obj.id} content to '{default_lang}' folder.")

    # restore default page
    if default_page:
        lrf.setDefaultPage(default_page)
        logger.info(f"Restored default page on '{default_lang}' folder.")

    # create navigation links in new LRFs
    root_folders = portal.listFolderContents(contentFilter={"portal_type": "LRF"})
    for lrf in root_folders:
        lang = lrf.id
        if lang == default_lang:
            continue
        add_navigation_links(lrf, lrf.id)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
