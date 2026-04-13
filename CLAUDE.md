# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python SDK for the SiliconFlow API (https://api.siliconflow.cn/v1/), providing async HTTP client functionality for embeddings, chat completions, image/audio/video generation, batch processing, and more.

## Development Environment

- **Python Version**: 3.12+ (specified in `.python-version`)
- **Package Manager**: uv (uses `pyproject.toml` and `uv.lock`)
- **Dependencies**: httpx>=0.28.1, orjson>=3.11.8

## Common Commands

```bash
# Install dependencies
uv sync

# Run a Python script with the environment
uv run python <script.py>

# Add a new dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Code linting (must pass before committing)
ruff check siliconflow/

# Type checking (optional)
pyright siliconflow/
```

## Architecture

### Namespace-Based API Organization

The `SiliconFlowClient` uses namespace-based organization for API categories:

```
SiliconFlowClient
├── text: TextAPI
│   ├── create_embed()      - Embeddings
│   ├── chat_completions()  - Chat completions (OpenAI format)
│   ├── chat_completions_anthropic()  - Chat completions (Anthropic format)
│   └── rerank()            - Rerank documents
├── image: ImageAPI
│   └── generations()       - Image generation
├── audio: AudioAPI
│   ├── transcriptions()    - Speech-to-text
│   ├── speech()            - Text-to-speech
│   ├── voice_list()        - List voice styles
│   ├── voice_upload()      - Upload voice reference
│   └── voice_delete()      - Delete voice reference
├── video: VideoAPI
│   ├── generations()       - Video generation
│   └── get_generation()    - Get video status
├── batch: BatchAPI
│   ├── create()            - Create batch job
│   ├── list()              - List batch jobs
│   ├── get()               - Get batch job details
│   ├── cancel()            - Cancel batch job
│   ├── upload_file()       - Upload file for batch
│   └── list_files()        - List uploaded files
└── platform: PlatformAPI
    └── list_models()       - List available models
```

### File Structure

```
siliconflow/
├── __init__.py          # Public exports (SiliconFlowClient, __version__)
├── client.py            # Main client class, initializes all API namespaces
├── _http.py             # HTTP client wrapper (httpx.AsyncClient + orjson)
├── _types.py            # TypedDict type definitions for all API requests/responses
└── api/
    ├── __init__.py      # API class exports
    ├── text.py          # TextAPI: embeddings, chat, rerank
    ├── image.py         # ImageAPI: image generation
    ├── audio.py         # AudioAPI: STT, TTS, voice management
    ├── video.py         # VideoAPI: video generation
    ├── batch.py         # BatchAPI: batch jobs and file management
    └── platform.py      # PlatformAPI: model listing
```

### Key Components

- **`siliconflow/client.py`**: Main entry point. Initializes HTTP client and all API namespaces (`self.text`, `self.image`, etc.)
- **`siliconflow/_http.py`**: HTTP client wrapper with automatic Bearer auth, orjson serialization, and connection pooling
- **`siliconflow/_types.py`**: Complete TypedDict definitions for all API request/response types
- **`siliconflow/api/*.py`**: Each file implements one API category class (e.g., `TextAPI`) with methods for that category's endpoints

### Design Patterns

1. **Namespace Organization**: APIs are grouped by category (`client.text`, `client.image`, etc.) for clear discovery
2. **Async-First**: All HTTP operations use `httpx.AsyncClient` with async/await
3. **Type Safety**: Full TypedDict coverage for all request/response structures
4. **JSON Performance**: Uses `orjson` for all JSON serialization/deserialization
5. **Streaming Support**: `chat_completions(stream=True)` returns `AsyncIterator`
6. **File Uploads**: Multipart form support for audio/video/batch file uploads via `post_form()`

### Usage Examples

```python
from siliconflow import SiliconFlowClient

async with SiliconFlowClient(key="your-api-key") as client:
    # Text embeddings
    result = await client.text.create_embed(
        model="BAAI/bge-m3",
        input="Hello, world!"
    )

    # Chat completion
    result = await client.text.chat_completions(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": "Hello"}]
    )

    # Image generation
    result = await client.image.generations(
        model="Kwai-Kolors/Kolors",
        prompt="a beautiful sunset"
    )

    # Speech-to-text
    with open("audio.mp3", "rb") as f:
        result = await client.audio.transcriptions(
            file=f,
            model="FunAudioLLM/SenseVoiceSmall"
        )
```

## Adding New API Endpoints

When adding a new endpoint:

1. Identify the correct category (text/image/audio/video/batch/platform)
2. Add TypedDict definitions to `_types.py` if new request/response types are needed
3. Add the method to the appropriate `api/<category>.py` file
4. Use `self._http.post()`/`get()`/`delete()`/`post_form()` for requests
5. Use `self._http.parse_json(response)` to deserialize responses
6. Run `ruff check siliconflow/` to ensure code quality
