"""Command-line interface for Code Roaster."""

import sys
from typing import Optional

import click

from code_roaster.config import Config, DEFAULT_PROVIDER
from code_roaster.formatters import TerminalFormatter
from code_roaster.llm_providers import get_provider
from code_roaster.roaster import CodeRoaster


@click.command()
@click.argument("file_path", type=click.Path(exists=True), required=False)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openai", "anthropic", "ollama", "openrouter"], case_sensitive=False),
    default=DEFAULT_PROVIDER,
    help="LLM provider to use for roasting",
)
@click.option(
    "--api-endpoint",
    "-e",
    help="Custom API endpoint URL",
)
@click.option(
    "--model",
    "-m",
    help="Model name to use (provider-specific, overrides environment variable settings)",
)
@click.option(
    "--list-providers",
    "-l",
    is_flag=True,
    help="List available LLM providers",
)
@click.version_option()
def main(
    file_path: str,
    provider: str,
    api_endpoint: Optional[str],
    model: Optional[str],
    list_providers: bool,
) -> None:
    """Roast a code file using AI.

    FILE_PATH is the path to the code file to roast.
    """
    formatter = TerminalFormatter()

    # If --list-providers is specified, display available providers and exit
    if list_providers:
        providers = Config.get_available_providers()
        formatter.display_provider_status(providers)
        return

    # Ensure file_path is provided if not listing providers
    if not file_path:
        formatter.display_error("File path is required when not using --list-providers")
        sys.exit(1)

    try:
        # Get the LLM provider
        llm_provider = get_provider(
            provider_name=provider,
            api_endpoint=api_endpoint,
            model_name=model,
        )

        # Create the code roaster
        roaster = CodeRoaster(llm_provider)

        # Display info message
        model_info = f" with model {model}" if model else ""
        formatter.display_info(f"Roasting {file_path} using {provider.capitalize()}{model_info}...")

        # Roast the code
        code_content, roast_content, language = roaster.roast_code(file_path)

        # Format and display the results
        formatter.format_roast(
            code_content=code_content,
            roast_content=roast_content,
            language=language,
            file_path=file_path,
        )

    except FileNotFoundError as e:
        formatter.display_error(str(e))
        sys.exit(1)
    except ValueError as e:
        formatter.display_error(str(e))
        sys.exit(1)
    except Exception as e:
        formatter.display_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()  # pragma: no cover