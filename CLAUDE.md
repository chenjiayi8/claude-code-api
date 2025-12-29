# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code API Gateway** - a Python FastAPI service that provides OpenAI-compatible API endpoints while leveraging Claude Code's CLI capabilities. It acts as a bridge between OpenAI-compatible clients and the Claude Code CLI tool, enabling developers to use Claude models through familiar OpenAI API patterns.

## Project Location

**Workspace Path**: `/home/frank/Growatt/Workspaces/claude-code-api/`

The main application code is located in the `claude_code_api/` subdirectory.

## Development Commands

The project uses a Makefile for all development workflows. Key commands:

### Setup & Installation
```bash
make install         # Install production dependencies
make test           # Run all tests (includes real Claude integration)
make start          # Start development server with auto-reload
make start-prod     # Start production server
```

### Testing
```bash
make test-real      # Run end-to-end API tests (uses actual HTTP requests)
make test-fast      # Run tests excluding slow ones
```

### Code Quality
```bash
make clean          # Clean Python cache files
make kill PORT=8000 # Kill process on specific port
```

## Architecture & Key Components

### Core Flow
Request → FastAPI → ClaudeManager → Claude CLI → Parse → OpenAI-compatible Response

### Key Files
- `claude_code_api/main.py` - FastAPI app entry point with lifespan management, CORS, and global exception handling
- `claude_code_api/core/claude_manager.py` - Manages Claude Code subprocess execution and output parsing
- `claude_code_api/core/session_manager.py` - Handles session lifecycle and conversation history
- `claude_code_api/core/config.py` - Configuration management with auto-detection of Claude CLI path
- `claude_code_api/api/chat.py` - Main chat completions endpoint (OpenAI-compatible)
- `claude_code_api/utils/streaming.py` - Server-Sent Events implementation for streaming responses
- `claude_code_api/api/models.py` - Additional API models and endpoints
- `claude_code_api/models/claude.py` - Claude-specific models and utilities

### Architecture Pattern
Clean architecture with clear separation:
- **Web Layer**: FastAPI endpoints, middleware, serialization
- **Business Layer**: Session management, process management, auth/rate limiting
- **Data Layer**: SQLite with SQLAlchemy, session storage

## Important Implementation Details

### Claude Code Integration
- Uses `--output-format stream-json` for structured output from Claude CLI
- Runs Claude from project directories to maintain context
- Maintains Claude's session IDs for proper conversation continuation
- Uses `--dangerously-skip-permissions` for development mode

### Streaming Support
- Claude produces JSONL output that's consumed line-by-line
- Each JSON object is converted to OpenAI streaming chunks
- SSE format ensures EventSource compatibility
- Handles backpressure to prevent memory issues

### Session Management
- UUID-based session identifiers
- Project context isolation (sessions tied to specific projects)
- Automatic timeout and cleanup
- Conversation history persistence in SQLite

### Configuration
- Auto-detects Claude binary path (PATH, npm global, common locations)
- Pydantic settings with environment variable support
- Authentication can be disabled with `REQUIRE_AUTH=false`
- CORS configuration for allowed origins

## Supported Models
Only Claude models (no OpenAI model aliases):
- `claude-opus-4-5-20251101` (Latest)
- `claude-opus-4-20250514`
- `claude-sonnet-4-20250514`
- `claude-3-7-sonnet-20250219`
- `claude-3-5-haiku-20241022`
- Custom models from environment variables

### Model Information
- **Opus 4.5**: Latest frontier model with enhanced reasoning (claude-opus-4-5-20251101)
- **Opus 4**: Most powerful model for complex reasoning (500K tokens, $15/$75 per 1K input/output)
- **Sonnet 4**: Latest Sonnet with enhanced capabilities (500K tokens, $3/$15 per 1K input/output)
- **Sonnet 3.7**: Advanced model for complex tasks (200K tokens, $3/$15 per 1K input/output)
- **Haiku 3.5**: Fast and cost-effective for quick tasks (200K tokens, $0.25/$1.25 per 1K input/output)

## Testing Approach
- Tests use real Claude Code CLI (no mocking for core functionality)
- Integration tests verify actual API endpoints with HTTP requests
- Temporary project directories used for test isolation
- Authentication disabled in test mode

## Development Notes
- All database operations are async (aiosqlite)
- Structured logging with JSON output using structlog
- OpenAI API format strictly followed for compatibility
- Rate limiting and authentication middleware included
- Health check verifies Claude CLI availability
- Comprehensive model validation and information system
- Tool usage tracking and metrics collection

## Environment Setup

The project uses a virtual environment located at `env/` in the project root. To activate it:

```bash
source env/bin/activate  # On Windows: env\Scripts\activate
```

The database file (`claude_api.db`) is created in the project root when the application starts.

## Demo & Documentation

- `demo.ipynb` - Jupyter notebook demonstrating API usage
- `docs/` - Additional documentation and examples
- `assets/` - Static assets and resources