# -*- coding: utf-8 -*-

from AccessControl import allow_module, allow_class, allow_type
from requests.models import Response

import imio.smartweb.policy.monkey  # noqa: F401


# Useful for code used in RestrictedPython (collective.themefragments)
allow_module("requests")
allow_class(Response)
allow_type(type("requests.models.Response"))
