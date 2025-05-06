"""Tests for the config module."""

import os
import unittest
from unittest.mock import patch

from code_roaster.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""

    def setUp(self):
        """Set up test environment."""
        # Clear any environment variables that might interfere with tests
        for var in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY"]:
            if var in os.environ:
                del os.environ[var]

    def test_get_api_key_not_found(self):
        """Test get_api_key when the key is not found."""
        # Ensure the environment variable is not set
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]

        # The method should return None
        self.assertIsNone(Config.get_api_key("openai"))

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_get_api_key_found(self):
        """Test get_api_key when the key is found."""
        # The method should return the key
        self.assertEqual(Config.get_api_key("openai"), "test_key")

    def test_get_api_endpoint_default(self):
        """Test get_api_endpoint with default values."""
        # Ensure the environment variable is not set
        if "OPENAI_API_ENDPOINT" in os.environ:
            del os.environ["OPENAI_API_ENDPOINT"]

        # The method should return the default endpoint
        self.assertEqual(
            Config.get_api_endpoint("openai"), "https://api.openai.com/v1"
        )

    @patch.dict(os.environ, {"OPENAI_API_ENDPOINT": "https://custom.endpoint.com"})
    def test_get_api_endpoint_from_env(self):
        """Test get_api_endpoint when the endpoint is set in the environment."""
        # The method should return the endpoint from the environment
        self.assertEqual(
            Config.get_api_endpoint("openai"), "https://custom.endpoint.com"
        )

    def test_get_api_endpoint_custom(self):
        """Test get_api_endpoint with a custom endpoint."""
        # The method should return the custom endpoint
        self.assertEqual(
            Config.get_api_endpoint("openai", "https://another.endpoint.com"),
            "https://another.endpoint.com",
        )

    def test_get_available_providers(self):
        """Test get_available_providers."""
        # Ollama should always be available
        providers = Config.get_available_providers()
        self.assertTrue(providers["ollama"])


if __name__ == "__main__":
    unittest.main()