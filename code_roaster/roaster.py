"""Core roasting functionality for Code Roaster."""

import os
from pathlib import Path
from typing import Optional, Tuple

from code_roaster.llm_providers import LLMProvider


class CodeRoaster:
    """Core functionality for roasting code files."""

    # Mapping of file extensions to language names
    LANGUAGE_EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "jsx",
        ".tsx": "tsx",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".cs": "csharp",
        ".go": "go",
        ".rb": "ruby",
        ".php": "php",
        ".swift": "swift",
        ".kt": "kotlin",
        ".rs": "rust",
        ".sh": "bash",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".sql": "sql",
        ".r": "r",
        ".dart": "dart",
    }

    def __init__(self, llm_provider: LLMProvider):
        """Initialize the code roaster.

        Args:
            llm_provider: The LLM provider to use for roasting
        """
        self.llm_provider = llm_provider

    def roast_code(self, file_path: str) -> Tuple[str, str, str]:
        """Roast the code in the specified file.

        Args:
            file_path: Path to the code file to roast

        Returns:
            A tuple containing (code_content, roast_content, language)

        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file type is not supported
        """
        # Read the code file
        code_content = self._read_code_file(file_path)

        # Detect the programming language
        language = self._detect_language(file_path)

        # Generate the roast
        roast_content = self.llm_provider.generate_roast(code_content, language)

        return code_content, roast_content, language

    def _read_code_file(self, file_path: str) -> str:
        """Read the content of a code file.

        Args:
            file_path: Path to the code file

        Returns:
            The content of the file as a string

        Raises:
            FileNotFoundError: If the file does not exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def _detect_language(self, file_path: str) -> str:
        """Detect the programming language of a file based on its extension.

        Args:
            file_path: Path to the code file

        Returns:
            The detected programming language

        Raises:
            ValueError: If the file extension is not supported
        """
        _, ext = os.path.splitext(file_path.lower())
        language = self.LANGUAGE_EXTENSIONS.get(ext)

        if not language:
            raise ValueError(
                f"Unsupported file extension: {ext}. "
                f"Supported extensions: {', '.join(self.LANGUAGE_EXTENSIONS.keys())}"
            )

        return language