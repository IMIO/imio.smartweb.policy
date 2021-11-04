# -*- coding: utf-8 -*-

from plone import api
import logging

logger = logging.getLogger("imio.smartweb.policy")
PROFILEID = "profile-imio.smartweb.policy:default"


def configure_first_official_release(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile("profile-pas.plugins.imio:default")
    context.runImportStepFromProfile(PROFILEID, "typeinfo")
    context.runImportStepFromProfile(PROFILEID, "viewlets")
