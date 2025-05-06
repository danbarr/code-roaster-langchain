"""LLM provider implementations for Code Roaster."""

import os
from abc import ABC, abstractmethod
from typing import Optional

from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from code_roaster.config import Config


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(
        self, api_endpoint: Optional[str] = None, model_name: Optional[str] = None
    ):
        """Initialize the LLM provider.

        Args:
            api_endpoint: Optional custom API endpoint
            model_name: Optional model name to use
        """
        self.api_endpoint = api_endpoint
        self.model_name = model_name
        self.llm = None
        self.initialize()

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the LLM client."""
        pass

    def generate_roast(self, code_content: str, language: str) -> str:
        """Generate a roast for the given code content.

        Args:
            code_content: The code content to roast
            language: The programming language of the code

        Returns:
            The generated roast
        """
        if not self.llm:
            raise ValueError("LLM client not initialized")

        prompt = self._create_prompt(code_content, language)
        
        try:
            # Check if the LLM is streaming
            if hasattr(self.llm, 'streaming') and self.llm.streaming:
                # Handle streaming response
                chunks = []
                for chunk in self.llm.stream(prompt):
                    if hasattr(chunk, 'content'):
                        chunks.append(chunk.content)
                    elif isinstance(chunk, str):
                        chunks.append(chunk)
                    else:
                        # Try to extract content from other response types
                        try:
                            chunks.append(str(chunk))
                        except:
                            pass
                return ''.join([c for c in chunks if c])
            else:
                # Handle non-streaming response
                response = self.llm.invoke(prompt)
                
                # Handle different response types
                if hasattr(response, 'content'):
                    # For ChatOllama and other chat models that return a message object
                    return response.content
                elif isinstance(response, str):
                    # For models that return a string directly
                    return response
                else:
                    # For other response types, convert to string
                    return str(response)
        except Exception as e:
            # If there's an error during streaming or processing, convert it to a string
            # This will include any CodeGate messages that might be in the error
            return str(e)

    def _create_prompt(self, code_content: str, language: str) -> str:
        """Create a prompt for the LLM.

        Args:
            code_content: The code content to roast
            language: The programming language of the code

        Returns:
            The formatted prompt
        """
        template = """
You are a code roaster who provides lighthearted, PG-rated jokes about code.
Analyze the following {language} code and create a humorous roast focusing on code structure and patterns.
Keep your comments funny but not mean-spirited.

CODE:
```{language}
{code_content}
```

Provide your roast with specific references to the code. Be creative and funny, but keep it PG-rated.
Focus on making general jokes about code structure and patterns.
Your response should be formatted as a cohesive roast, not a list of issues.
"""
        prompt_template = PromptTemplate.from_template(template)
        return prompt_template.format(code_content=code_content, language=language)


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def initialize(self) -> None:
        """Initialize the OpenAI client."""
        api_key = Config.get_api_key("openai")
        if not api_key:
            raise ValueError("OpenAI API key not found")

        api_endpoint = self.api_endpoint or Config.get_api_endpoint("openai")
        model_name = self.model_name or Config.get_model("openai")

        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url=api_endpoint,
            model_name=model_name,
            temperature=0.7,
            streaming=True,  # Enable streaming for proxies that force streaming mode
        )


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider implementation."""

    def initialize(self) -> None:
        """Initialize the Anthropic client."""
        api_key = Config.get_api_key("anthropic")
        if not api_key:
            raise ValueError("Anthropic API key not found")

        api_endpoint = self.api_endpoint or Config.get_api_endpoint("anthropic")
        model_name = self.model_name or Config.get_model("anthropic")

        self.llm = ChatAnthropic(
            api_key=api_key,
            base_url=api_endpoint,
            model_name=model_name,
            temperature=0.7,
            streaming=True,  # Enable streaming mode
        )


class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation."""

    def initialize(self) -> None:
        """Initialize the Ollama client."""
        api_endpoint = self.api_endpoint or Config.get_api_endpoint("ollama")
        model_name = self.model_name or Config.get_model("ollama")

        self.llm = ChatOllama(
            base_url=api_endpoint,
            model=model_name,
            temperature=0.7,
            streaming=True,  # Enable streaming mode
        )


class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider implementation."""

    def initialize(self) -> None:
        """Initialize the OpenRouter client."""
        api_key = Config.get_api_key("openrouter")
        if not api_key:
            raise ValueError("OpenRouter API key not found")

        api_endpoint = self.api_endpoint or Config.get_api_endpoint("openrouter")
        model_name = self.model_name or Config.get_model("openrouter")

        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url=api_endpoint,
            model_name=model_name,
            temperature=0.7,
            streaming=True,  # Enable streaming for proxies that force streaming mode
        )


def get_provider(
    provider_name: str,
    api_endpoint: Optional[str] = None,
    model_name: Optional[str] = None,
) -> LLMProvider:
    """Get an LLM provider instance based on the provider name.

    Args:
        provider_name: The name of the LLM provider
        api_endpoint: Optional custom API endpoint
        model_name: Optional model name to use

    Returns:
        An instance of the specified LLM provider

    Raises:
        ValueError: If the provider name is not supported
    """
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
        "openrouter": OpenRouterProvider,
    }

    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unsupported provider: {provider_name}")

    return provider_class(api_endpoint=api_endpoint, model_name=model_name)