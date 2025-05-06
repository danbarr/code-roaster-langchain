"""Configuration handling for Code Roaster."""

import os
from typing import Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default API endpoints
DEFAULT_ENDPOINTS = {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com",
    "ollama": "http://localhost:11434",
    "openrouter": "https://openrouter.ai/api/v1",
}

# Default models
DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "ollama": "llama3",
    "openrouter": "openai/gpt-4o-mini",
}

# Default provider
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openai")


class Config:
    """Configuration manager for Code Roaster."""

    @staticmethod
    def get_api_key(provider: str) -> Optional[str]:
        """Get the API key for the specified provider.

        Args:
            provider: The LLM provider name (openai, anthropic, openrouter)

        Returns:
            The API key if found, None otherwise
        """
        env_var_name = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var_name)

        if not api_key and provider != "ollama":
            print(f"Warning: No API key found for {provider}.")
            print(f"Please set the {env_var_name} environment variable.")

        return api_key

    @staticmethod
    def get_api_endpoint(provider: str, custom_endpoint: Optional[str] = None) -> str:
        """Get the API endpoint for the specified provider.

        Args:
            provider: The LLM provider name
            custom_endpoint: Optional custom endpoint to override the default

        Returns:
            The API endpoint URL
        """
        if custom_endpoint:
            return custom_endpoint

        env_var_name = f"{provider.upper()}_API_ENDPOINT"
        api_endpoint = os.getenv(env_var_name)

        if not api_endpoint:
            api_endpoint = DEFAULT_ENDPOINTS.get(provider.lower())

        if not api_endpoint:
            raise ValueError(f"No API endpoint found for provider: {provider}")

        return api_endpoint
        
    @staticmethod
    def get_model(provider: str, custom_model: Optional[str] = None) -> str:
        """Get the model name for the specified provider.

        Args:
            provider: The LLM provider name
            custom_model: Optional custom model to override the default

        Returns:
            The model name
        """
        if custom_model:
            return custom_model

        env_var_name = f"{provider.upper()}_MODEL"
        model = os.getenv(env_var_name)

        if not model:
            model = DEFAULT_MODELS.get(provider.lower())

        if not model:
            raise ValueError(f"No model found for provider: {provider}")

        return model

    @staticmethod
    def get_available_providers() -> Dict[str, bool]:
        """Get a dictionary of available providers and their availability status.

        Returns:
            A dictionary mapping provider names to their availability status
        """
        providers = {
            "openai": bool(Config.get_api_key("openai")),
            "anthropic": bool(Config.get_api_key("anthropic")),
            "ollama": True,  # Ollama doesn't require an API key
            "openrouter": bool(Config.get_api_key("openrouter")),
        }
        return providers