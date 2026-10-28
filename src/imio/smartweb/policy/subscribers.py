# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from plone import api

import transaction


def prevent_lrf_removal(obj, event):
    """Only Managers may delete a language root folder (LRF).

    Other removal subscribers (catalog unindexing, ...) have already run when
    this one raises, and some callers (folder_contents) swallow Unauthorized:
    dooming the transaction guarantees that nothing gets committed.
    """
    if "Manager" not in api.user.get_roles(obj=obj):
        transaction.doom()
        raise Unauthorized("Only Managers can delete a language root folder.")
