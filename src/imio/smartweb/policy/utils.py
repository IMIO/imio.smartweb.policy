# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate


def remove_unused_contents(portal):
    api.content.delete(portal.news)
    api.content.delete(portal.events)
    api.content.delete(portal.Members)


def clear_manager_portlets(folder, manager_name):
    manager = getUtility(IPortletManager, name=manager_name, context=folder)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]


def add_navigation_links(context):
    current_lang = api.portal.get_current_language()[:2]
    api.content.create(
        container=context,
        type="Link",
        title=translate(_(u"I am"), target_language=current_lang),
    )
    api.content.create(
        container=context,
        type="Link",
        title=translate(_(u"One click finding"), target_language=current_lang),
    )
