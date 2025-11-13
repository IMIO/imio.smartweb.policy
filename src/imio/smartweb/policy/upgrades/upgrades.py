# -*- coding: utf-8 -*-

from imio.smartweb.policy.utils import add_iam_folder
from plone import api
from plone.app.workflow.remap import remap_workflow
from Products.CMFPlone.utils import get_installer
import logging

logger = logging.getLogger("imio.smartweb.policy")
PROFILEID = "profile-imio.smartweb.policy:default"


def configure_first_official_release(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile("profile-pas.plugins.imio:default")
    portal_setup.runImportStepFromProfile(PROFILEID, "typeinfo")
    portal_setup.runImportStepFromProfile(PROFILEID, "viewlets")


def reload_types(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "typeinfo")


def transform_old_iam_link_to_iam_folder(context):
    portal = api.portal.get()
    obj = portal.get("i-am") or portal.get("je-suis")
    if obj is not None:
        if obj.portal_type != "Link":
            return
        else:
            api.content.delete(obj=obj)
    current_lang = api.portal.get_current_language()[:2]
    add_iam_folder(portal, current_lang)


def restore_links_workflow(context):
    portal = api.portal.get()
    remap_workflow(portal, type_ids=("Link",), chain="(Default)")


def reload_viewlets(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "viewlets")


def uninstall_z3cform_select2(context):
    installer = get_installer(context)
    installer.uninstall_product("collective.z3cform.select2")


def install_kimug(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runAllImportStepsFromProfile("profile-pas.plugins.kimug:default")


def set_keycloak_login_group(context):
    acl_users = api.portal.get_tool("acl_users")
    oidc = acl_users.get("oidc")
    if oidc is not None:
        oidc.allowed_groups = ["iA.Smartweb"]
    else:
        logger.warning("OIDC plugin not found in acl_users; cannot set allowed_groups.")


def uninstall_plone_patternslib(context):
    product = "plone.patternslib"
    installer = get_installer(context)
    if not installer.is_product_installable(product):
        # plone.patternslib is not present on all instance ?!
        return
    if installer.is_product_installed(product):
        installer.uninstall_product("plone.patternslib")
