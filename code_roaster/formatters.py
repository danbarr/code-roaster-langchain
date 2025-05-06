"""Terminal output formatting for Code Roaster."""

from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text


class TerminalFormatter:
    """Format roast results for terminal display with colors and styling."""

    def __init__(self):
        """Initialize the formatter with a Rich console."""
        self.console = Console()

    def format_roast(
        self, code_content: str, roast_content: str, language: str, file_path: str
    ) -> None:
        """Format and display the roast results in the terminal.

        Args:
            code_content: The original code content
            roast_content: The roast content from the LLM
            language: The programming language of the code
            file_path: The path to the roasted file
        """
        # Display a header with the file path
        self.console.print()
        self.console.print(
            f"[bold cyan]Code Roaster[/bold cyan] - Roasting [bold yellow]{file_path}[/bold yellow]"
        )
        self.console.print()

        # Display the original code with syntax highlighting
        self.console.print("[bold green]Original Code:[/bold green]")
        syntax = Syntax(
            code_content, language, theme="monokai", line_numbers=True, word_wrap=True
        )
        self.console.print(Panel(syntax, expand=False))
        self.console.print()

        # Display the roast
        self.console.print("[bold red]🔥 The Roast 🔥[/bold red]")
        roast_panel = Panel(
            Text(roast_content, style="bold"),
            border_style="red",
            title="Code Roaster",
            title_align="center",
        )
        self.console.print(roast_panel)
        self.console.print()

    def display_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message to display
        """
        self.console.print(f"[bold red]Error:[/bold red] {message}")

    def display_warning(self, message: str) -> None:
        """Display a warning message.

        Args:
            message: The warning message to display
        """
        self.console.print(f"[bold yellow]Warning:[/bold yellow] {message}")

    def display_info(self, message: str) -> None:
        """Display an informational message.

        Args:
            message: The info message to display
        """
        self.console.print(f"[bold blue]Info:[/bold blue] {message}")

    def display_success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: The success message to display
        """
        self.console.print(f"[bold green]Success:[/bold green] {message}")

    def display_provider_status(self, providers: Dict[str, bool]) -> None:
        """Display the status of available LLM providers.

        Args:
            providers: A dictionary mapping provider names to their availability status
        """
        self.console.print("[bold cyan]Available LLM Providers:[/bold cyan]")
        for provider, available in providers.items():
            status = "[green]✓[/green]" if available else "[red]✗[/red]"
            self.console.print(f"  {status} {provider.capitalize()}")
        self.console.print()