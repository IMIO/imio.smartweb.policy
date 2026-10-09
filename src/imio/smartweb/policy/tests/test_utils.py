# -*- coding: utf-8 -*-
"""Setup tests for this package."""

from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)  # noqa: E501
from imio.smartweb.policy.utils import get_ts_api_base_url
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from unittest.mock import MagicMock
from unittest.mock import patch

import os
import unittest


class TestUtils(unittest.TestCase):
    """Test that imio.smartweb.policy is properly installed."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal.setLanguage("fr")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _check_iam_links_start_with(self, base_url, iam_folder, delete=False):
        for link in api.content.find(context=iam_folder, portal_type="Link", depth=1):
            link_obj = link.getObject()
            url_token = link_obj.remoteUrl.split("iam=")[-1]
            assert link_obj.remoteUrl == f"{base_url}{url_token}"
            if delete:
                api.content.delete(link_obj)

    def test_add_iam_folder(self):
        """Test add_iam_folder utility."""
        from imio.smartweb.policy.utils import add_iam_folder

        os.environ.pop("WEBSITE_HOSTNAME", None)

        # 1. Add iam folder without WEBSITE_HOSTNAME set
        add_iam_folder(self.portal, "fr")

        self.assertIn("je-suis", self.portal)

        iam_folder = self.portal["je-suis"]
        self._check_iam_links_start_with(
            "/Plone/@@search?iam=", iam_folder, delete=True
        )
        api.content.delete(iam_folder)

        # 2. Add iam folder with WEBSITE_HOSTNAME set
        os.environ["WEBSITE_HOSTNAME"] = "www.kamoulox.be"
        add_iam_folder(self.portal, "fr")
        iam_folder = self.portal["je-suis"]
        self._check_iam_links_start_with(
            "https://www.kamoulox.be/@@search?iam=", iam_folder, delete=True
        )
        api.content.delete(iam_folder)

    def test_update_iam_folder_links(self):
        """Test update_iam_folder_links utility."""
        from imio.smartweb.policy.utils import add_iam_folder
        from imio.smartweb.policy.utils import update_iam_folder_links

        os.environ.pop("WEBSITE_HOSTNAME", None)

        # 1. Add iam folder without WEBSITE_HOSTNAME set
        add_iam_folder(self.portal, "fr")
        iam_folder = self.portal["je-suis"]
        base_url = "/Plone/@@search?iam="
        self._check_iam_links_start_with(base_url, iam_folder)

        # 2. Update links with WEBSITE_HOSTNAME set
        os.environ["WEBSITE_HOSTNAME"] = "www.kamoulox.be"
        update_iam_folder_links(iam_folder, commit=False)
        base_url = "https://www.kamoulox.be/@@search?iam="
        self._check_iam_links_start_with(base_url, iam_folder)

        # 3. Removing WEBSITE_HOSTNAME and updating links again
        os.environ.pop("WEBSITE_HOSTNAME", None)
        update_iam_folder_links(iam_folder, commit=False)
        base_url = "/Plone/@@search?iam="
        self._check_iam_links_start_with(base_url, iam_folder)

        # 4. Delete a link and update links again, link should not be there anymore
        link = api.content.get(path="/je-suis/jeune")
        api.content.delete(link)
        update_iam_folder_links(iam_folder, commit=False)
        assert not api.content.get(path="/je-suis/jeune")
        base_url = "/Plone/@@search?iam="
        self._check_iam_links_start_with(base_url, iam_folder)

        # 5. Changing a link remoteUrl to a non standard format and updating links again, link should be unchanged
        os.environ["WEBSITE_HOSTNAME"] = "www.kamoulox.com"
        link = api.content.get(path="/je-suis/commercant")
        link.remoteUrl = "https://www.kamoulox.be/commercant"
        link.reindexObject()
        update_iam_folder_links(iam_folder, commit=False)
        link = api.content.get(path="/je-suis/commercant")
        assert link.remoteUrl == "https://www.kamoulox.be/commercant"


class TestUpdateIamFolderLinksStartup(unittest.TestCase):

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def test_startup_connection_closed_when_site_missing(self):
        """At startup without a Plone site, the connection opened to look for it
        must be closed: a leaked one keeps its storage read snapshot open."""
        from imio.smartweb.policy import utils

        conn = MagicMock()
        conn.root.return_value = {"Application": {}}
        context = MagicMock()
        context.database.open.return_value = conn
        with patch.object(
            utils.api.portal, "get", side_effect=api.exc.CannotGetPortalError
        ):
            utils.update_iam_folder_links(context)
        conn.close.assert_called_once()

    def test_startup_connection_closed_after_update(self):
        """At startup with a Plone site, the links are updated, then the
        transaction is aborted, the site unset and the connection closed."""
        from imio.smartweb.policy import utils

        site = object()
        conn = MagicMock()
        conn.root.return_value = {"Application": {"Plone": site}}
        context = MagicMock()
        context.database.open.return_value = conn
        with patch.object(
            utils.api.portal, "get", side_effect=api.exc.CannotGetPortalError
        ), patch("imio.smartweb.policy.utils.setSite") as mock_set_site, patch(
            "imio.smartweb.policy.utils._update_iam_folder_links"
        ) as mock_update, patch(
            "imio.smartweb.policy.utils.transaction"
        ) as mock_transaction:
            utils.update_iam_folder_links(context)
        mock_update.assert_called_once_with(site, True)
        assert [c.args for c in mock_set_site.call_args_list] == [(site,), (None,)]
        mock_transaction.abort.assert_called_once()
        conn.close.assert_called_once()


class TestGetTsApiBaseUrl(unittest.TestCase):

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    @patch("imio.smartweb.core.utils.get_value_from_registry")
    @patch("imio.smartweb.core.utils.is_valid_url")
    @patch("imio.smartweb.policy.utils.urlparse")
    def test_valid_url(self, mock_urlparse, mock_is_valid_url, mock_get_value):
        mock_get_value.return_value = "https://kamoulox.be/formsdefs/something"
        mock_is_valid_url.return_value = True
        mock_urlparse.return_value.scheme = "https"
        mock_urlparse.return_value.netloc = "kamoulox.be"
        result = get_ts_api_base_url()
        self.assertEqual(result, "https://kamoulox.be/")

    @patch("imio.smartweb.core.utils.get_value_from_registry")
    @patch("imio.smartweb.core.utils.is_valid_url")
    def test_invalid_url(self, mock_is_valid_url, mock_get_value):
        mock_get_value.return_value = "not-a-valid-url"
        mock_is_valid_url.return_value = False
        result = get_ts_api_base_url()
        self.assertIsNone(result)

    @patch("imio.smartweb.core.utils.get_value_from_registry")
    @patch("imio.smartweb.core.utils.is_valid_url")
    def test_empty_url(self, mock_is_valid_url, mock_get_value):
        mock_get_value.return_value = ""
        mock_is_valid_url.return_value = False
        result = get_ts_api_base_url()
        self.assertIsNone(result)
