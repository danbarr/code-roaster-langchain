# Code Roaster

A CLI tool that takes a code file and roasts it using AI. The roasts are
lighthearted and PG-rated, focusing on general jokes about code structure and
patterns.

This is a demonstration app meant to show off how to use CodeGate with an LLM
framework like LangChain.

## About CodeGate

[CodeGate](https://github.com/stacklok/codegate) is a local prompt gateway that
sits between an AI application/agent and the LLM to enhance privacy and
security. CodeGate prevents sensitive data like secrets and PII from being
shared with AI providers and provides security analysis of AI-generated code
including detection of malicious and deprecated packages.

It also provides a centralized, abstracted environment for managing prompts,
model provider configurations, model muxing, and more.

The `example_code.py` file in this repository is a sample code file that is
intentionally written to trigger CodeGate's filters. It contains a deprecated
package, hardcoded secrets, and PII data.

## Installation

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management (recommended)

### Using uv (recommended)

```bash
# Install uv if not already installed
pip install uv

# Clone the repository
git clone https://github.com/danbarr/code-roaster.git
cd code-roaster

# Create a virtual environment
uv venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate

# Install the package
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/code-roaster.git
cd code-roaster

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install the package
pip install -e .
```

## Configuration

1. Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API keys for the LLM providers you want to
   use. You can also configure the model for each provider. If you don't want to
   save your keys to the `.env` file (understandable!), you can set them as
   environment variables in your shell instead.

### Environment Variables

For each provider, you can configure:

- API key (except for Ollama)
- API endpoint
- Model name

Example (see `.env.example` for complete example):

```text
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_API_ENDPOINT=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

# Ollama Configuration
OLLAMA_API_ENDPOINT=http://localhost:11434
OLLAMA_MODEL=mistral-nemo
```

Example configuration for use with CodeGate (see `.env.codegate-example` for
complete example):

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_ENDPOINT=http://localhost:8989/openai
OPENAI_MODEL=gpt-4o-mini

# Ollama Configuration
OLLAMA_API_ENDPOINT=http://localhost:8989/ollama
OLLAMA_MODEL=mistral-nemo
```

## Usage

```bash
# Basic usage with default provider (specified in .env)
code-roaster path/to/file.py

# Specify a different provider
code-roaster --provider ollama path/to/file.py

# Override API endpoint
code-roaster --provider openai --api-endpoint https://custom-endpoint.example.com/v1 path/to/file.py

# Specify a different model
code-roaster --provider ollama --model mistral path/to/file.py

# List available providers
code-roaster --list-providers

# Display help
code-roaster --help
```

## Supported LLM Providers

- **OpenAI**: Requires an API key

  - Default model: gpt-4o-mini

- **Anthropic**: Requires an API key

  - Default model: claude-3-5-haiku-latest

- **Ollama**: Local LLM, no API key required

  - Default model: llama3

- **OpenRouter**: Requires an API key
  - Default model: openai/gpt-4o-mini

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for details.
