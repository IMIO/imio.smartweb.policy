from imio.smartweb.policy.testing import (
    IMIO_SMARTWEB_POLICY_INTEGRATION_TESTING,
)  # noqa: E501
from unittest.mock import patch
from imio.smartweb.policy.utils import get_ts_api_base_url

import unittest


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
