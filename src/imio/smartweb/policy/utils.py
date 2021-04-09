# -*- coding: utf-8 -*-

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility


def clear_manager_portlets(folder, manager_name):
    manager = getUtility(IPortletManager, name=manager_name, context=folder)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]
