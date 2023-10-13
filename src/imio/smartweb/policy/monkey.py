# -*- coding: utf-8 -*-
from collective.pivot.config import getFamilyProperties
from collective.pivot.utils import _
from collective.pivot.utils import add_family
from collective.pivot import setuphandlers
from plone import api


def pivot_post_install(context):
    """Post install script"""
    current_lang = api.portal.get_current_language()[:2]
    site = api.portal.get()
    if not site.get("PIVOT"):
        folder = api.content.create(
            type="imio.smartweb.Folder",
            container=site,
            title=_("PIVOT", context=site, target_language=current_lang),
        )
        pivot_add_default_categories(folder)


setuphandlers.post_install = pivot_post_install


def pivot_add_default_categories(context):
    """Add Pivot categories"""
    current_lang = api.portal.get_current_language()[:2]
    add_family(
        context,
        family_id=getFamilyProperties().get("hosting").get("urn"),
        title=_("Hosting", context=context, target_language=current_lang),
    )
    add_family(
        context,
        family_id=getFamilyProperties().get("leisure").get("urn"),
        title=_("Leisure / discovery", context=context, target_language=current_lang),
    )
    add_family(
        context,
        family_id=getFamilyProperties().get("tourism_organizations").get("urn"),
        title=_("Tourism organizations", context=context, target_language=current_lang),
    )
    add_family(
        context,
        family_id=getFamilyProperties().get("events").get("urn"),
        title=_("Events", context=context, target_language=current_lang),
    )
    add_family(
        context,
        family_id=getFamilyProperties().get("terroir").get("urn"),
        title=_("Terroir", context=context, target_language=current_lang),
    )
