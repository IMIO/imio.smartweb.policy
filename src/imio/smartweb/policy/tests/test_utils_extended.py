# -*- coding: utf-8 -*-
"""Extended tests for utils.py module."""
from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)
from imio.smartweb.policy.utils import add_iam_folder
from imio.smartweb.policy.utils import add_ifind_folder
from imio.smartweb.policy.utils import add_navigation_links
from imio.smartweb.policy.utils import clear_manager_portlets
from imio.smartweb.policy.utils import get_cookie_policy_content
from imio.smartweb.policy.utils import get_gdpr_html_content
from imio.smartweb.policy.utils import remove_unused_contents
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from unittest.mock import MagicMock
from unittest.mock import patch
from z3c.form.interfaces import IFormLayer
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


class TestRemoveUnusedContents(unittest.TestCase):
    """Test remove_unused_contents function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_remove_unused_contents_deletes_default_folders(self):
        """Test that remove_unused_contents deletes default Plone folders."""
        # Create the default folders if they don't exist
        if not hasattr(self.portal, "news"):
            api.content.create(
                container=self.portal, type="Folder", id="news", title="News"
            )
        if not hasattr(self.portal, "events"):
            api.content.create(
                container=self.portal, type="Folder", id="events", title="Events"
            )
        if not hasattr(self.portal, "Members"):
            api.content.create(
                container=self.portal, type="Folder", id="Members", title="Members"
            )

        # Verify they exist
        self.assertTrue(hasattr(self.portal, "news"))
        self.assertTrue(hasattr(self.portal, "events"))
        self.assertTrue(hasattr(self.portal, "Members"))

        # Remove them
        remove_unused_contents(self.portal)

        # Verify they're gone
        self.assertFalse(hasattr(self.portal, "news"))
        self.assertFalse(hasattr(self.portal, "events"))
        self.assertFalse(hasattr(self.portal, "Members"))


class TestClearManagerPortlets(unittest.TestCase):
    """Test clear_manager_portlets function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_clear_manager_portlets_removes_all_portlets(self):
        """Test that clear_manager_portlets removes all portlets from a manager."""
        manager_name = "plone.leftcolumn"
        manager = getUtility(IPortletManager, name=manager_name, context=self.portal)
        assignments = getMultiAdapter(
            (self.portal, manager), IPortletAssignmentMapping
        )

        # Add a test portlet if none exist
        from plone.portlets.interfaces import IPortletAssignment

        if len(assignments) == 0:
            # Create a simple mock portlet
            mock_portlet = MagicMock(spec=IPortletAssignment)
            assignments["test-portlet"] = mock_portlet

        initial_count = len(assignments)
        self.assertGreaterEqual(initial_count, 0)

        # Clear portlets
        clear_manager_portlets(self.portal, manager_name)

        # Verify all portlets are removed
        self.assertEqual(len(assignments), 0)

    def test_clear_manager_portlets_with_multiple_managers(self):
        """Test clearing portlets from multiple managers."""
        managers = ["plone.leftcolumn", "plone.rightcolumn", "plone.footerportlets"]

        for manager_name in managers:
            manager = getUtility(IPortletManager, name=manager_name, context=self.portal)
            assignments = getMultiAdapter(
                (self.portal, manager), IPortletAssignmentMapping
            )

            # Clear portlets
            clear_manager_portlets(self.portal, manager_name)

            # Verify all portlets are removed
            self.assertEqual(len(assignments), 0)


class TestAddIamFolder(unittest.TestCase):
    """Test add_iam_folder function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("imio.smartweb.policy.utils.get_vocabulary")
    def test_add_iam_folder_creates_folder_and_links(self, mock_vocab):
        """Test that add_iam_folder creates folder with links."""
        # Mock vocabulary
        mock_term1 = MagicMock()
        mock_term1.token = "citizen"
        mock_term1.title = "Citizen"

        mock_term2 = MagicMock()
        mock_term2.token = "business"
        mock_term2.title = "Business"

        mock_vocab.return_value = [mock_term1, mock_term2]

        add_iam_folder(self.portal, "fr")

        # Verify folder was created
        self.assertTrue(hasattr(self.portal, "i-am"))
        iam_folder = getattr(self.portal, "i-am")

        # Verify folder is published
        state = api.content.get_state(obj=iam_folder)
        self.assertEqual(state, "published")

        # Verify links were created
        links = iam_folder.objectValues()
        self.assertEqual(len(links), 2)

        # Verify links have correct remote URLs
        for link in links:
            self.assertTrue(link.remoteUrl.startswith(self.portal.absolute_url()))
            self.assertIn("@@search?iam=", link.remoteUrl)


class TestAddIfindFolder(unittest.TestCase):
    """Test add_ifind_folder function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        alsoProvides(self.request, IFormLayer)

    def test_add_ifind_folder_creates_folder_and_collection(self):
        """Test that add_ifind_folder creates folder with collection."""
        add_ifind_folder(self.portal, "fr")

        # Verify folder was created
        self.assertTrue(hasattr(self.portal, "i-find"))
        ifind_folder = getattr(self.portal, "i-find")

        # Verify folder is published
        state = api.content.get_state(obj=ifind_folder)
        self.assertEqual(state, "published")

        # Verify collection was created
        collections = [
            obj for obj in ifind_folder.objectValues() if obj.portal_type == "Collection"
        ]
        self.assertEqual(len(collections), 1)

        collection = collections[0]
        # Verify collection is published
        state = api.content.get_state(obj=collection)
        self.assertEqual(state, "published")

        # Verify collection query
        self.assertIsNotNone(collection.query)
        self.assertTrue(len(collection.query) > 0)
        self.assertEqual(collection.query[0]["i"], "portal_type")


class TestAddNavigationLinks(unittest.TestCase):
    """Test add_navigation_links function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("imio.smartweb.policy.utils.add_iam_folder")
    @patch("imio.smartweb.policy.utils.add_ifind_folder")
    def test_add_navigation_links_calls_subfunctions(
        self, mock_ifind, mock_iam
    ):
        """Test that add_navigation_links calls both add_iam and add_ifind."""
        add_navigation_links(self.portal, "fr")

        mock_iam.assert_called_once_with(self.portal, "fr")
        mock_ifind.assert_called_once_with(self.portal, "fr")

    @patch("imio.smartweb.policy.utils.add_iam_folder")
    @patch("imio.smartweb.policy.utils.add_ifind_folder")
    @patch("imio.smartweb.policy.utils.api.portal.get_current_language")
    def test_add_navigation_links_uses_current_language(
        self, mock_lang, mock_ifind, mock_iam
    ):
        """Test that add_navigation_links uses current language when not specified."""
        mock_lang.return_value = "nl-BE"

        add_navigation_links(self.portal)

        mock_iam.assert_called_once_with(self.portal, "nl")
        mock_ifind.assert_called_once_with(self.portal, "nl")


class TestGetGdprHtmlContent(unittest.TestCase):
    """Test get_gdpr_html_content function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def test_get_gdpr_html_content_with_commune(self):
        """Test get_gdpr_html_content with a commune name."""
        result = get_gdpr_html_content("Test Commune")

        self.assertIn("Test Commune", result)
        self.assertIn("Déclaration relative à la protection des données", result)
        self.assertIn("RGPD", result)
        self.assertIn("<h1>", result)
        self.assertIn("<h2>", result)
        self.assertIn("<p>", result)

    def test_get_gdpr_html_content_without_commune(self):
        """Test get_gdpr_html_content without a commune name."""
        result = get_gdpr_html_content(None)

        self.assertIn("[nom du pouvoir local]", result)
        self.assertIn("Déclaration relative à la protection des données", result)

    def test_get_gdpr_html_content_structure(self):
        """Test that GDPR content has expected structure."""
        result = get_gdpr_html_content("My City")

        # Verify sections are present
        self.assertIn("I. Introduction", result)
        self.assertIn("II. À quelles fins", result)
        self.assertIn("III. Qui est le «responsable du traitement", result)
        self.assertIn("IV. À qui vos données sont-elles communiquées", result)
        self.assertIn("V. Combien de temps vos données sont-elles conservées", result)
        self.assertIn("VI. Comment consulter vos données", result)
        self.assertIn("VII. Quels sont les moyens", result)
        self.assertIn("VIII. À qui adresser des questions", result)

    def test_get_gdpr_html_content_data_protection_details(self):
        """Test GDPR content includes data protection details."""
        result = get_gdpr_html_content("Test City")

        self.assertIn("Règlement (UE) 2016/679", result)
        self.assertIn("Plausible", result)
        self.assertIn("iMio", result)


class TestGetCookiePolicyContent(unittest.TestCase):
    """Test get_cookie_policy_content function."""

    layer = IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING

    def test_get_cookie_policy_content_structure(self):
        """Test get_cookie_policy_content returns expected structure."""
        result = get_cookie_policy_content()

        self.assertIn("Politique d'utilisation des cookies", result)
        self.assertIn("cookies essentiels", result)
        self.assertIn("cookies fonctionnels", result)
        self.assertIn("<h1>", result)
        self.assertIn("<h2>", result)
        self.assertIn("<p>", result)
        self.assertIn("<ul>", result)
        self.assertIn("<li>", result)

    def test_get_cookie_policy_content_mentions_specific_cookies(self):
        """Test that specific cookies are mentioned in the policy."""
        result = get_cookie_policy_content()

        # Essential cookies
        self.assertIn("cc_cookie_accept", result)
        self.assertIn("serverid", result)
        self.assertIn("__ac", result)

        # Functional cookies
        self.assertIn("I18N_LANGUAGE", result)

        # YouTube cookies
        self.assertIn("YouTube", result)
        self.assertIn("1P_JAR", result)
        self.assertIn("CONSENT", result)

    def test_get_cookie_policy_content_mentions_management(self):
        """Test that cookie management instructions are present."""
        result = get_cookie_policy_content()

        self.assertIn("Gestion et suppression des cookies", result)
        self.assertIn("Firefox, Chrome, Edge", result)
        self.assertIn("CTRL/CMD", result)

    def test_get_cookie_policy_content_cookie_types(self):
        """Test that both cookie types are explained."""
        result = get_cookie_policy_content()

        # Essential cookies section
        self.assertIn("Cookies essentiels", result)
        self.assertIn("load balancing", result)

        # Functional cookies section
        self.assertIn("Cookies fonctionnels", result)
        self.assertIn("préférences en matière de langue", result)

    def test_get_cookie_policy_content_youtube_cookies_details(self):
        """Test that YouTube cookies are listed with expiration times."""
        result = get_cookie_policy_content()

        youtube_cookies = [
            "1P_JAR (1 mois)",
            "ANID (9 mois)",
            "APISID (2 ans)",
            "CONSENT (10 ans)",
            "SIDCC (1 an)",
        ]

        for cookie in youtube_cookies:
            self.assertIn(cookie, result)