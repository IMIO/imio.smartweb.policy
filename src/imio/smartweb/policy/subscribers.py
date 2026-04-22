# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from plone import api


def prevent_messages_config_delete(obj, event):
    """Only Managers may remove the global messages configuration folder."""
    if getattr(obj, "portal_type", None) != "MessagesConfig":
        return

    if "Manager" in api.user.get_roles(obj=obj):
        return

    raise Unauthorized("Only Managers can delete MessagesConfig objects.")
