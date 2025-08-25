# Project Handover Document

## Project Overview

- **Project Name**: godevopsid_bot
- **Repository**: github.com/prasetiyohadi/godevopsid_bot
- **Key Files**:
  - `main.py`: Main application entry point (FastAPI server, Telegram bot integration)
  - `devbox.json`: Configuration for development environment
  - `pyproject.toml`: Python project configuration
  - `README.md`: Project documentation

## Key Components

1. **Main Application (`main.py`)**
   - FastAPI server with endpoints for:
     - Root (`/`): Simple hello message
     - Notification (`/`): Handles POST requests to send Telegram messages
     - Health check (`/health`): Simple status endpoint
   - Environment variable management for Telegram bot token and channel ID
   - Custom logging configuration for Uvicorn
   - **Includes all Telegram notification logic**

2. **Development Configuration (`devbox.json`)**
   - Defines development environment settings
   - Includes dependencies and setup instructions

3. **Python Configuration (`pyproject.toml`)**
   - Specifies project dependencies and metadata

4. **Environment Setup (`env.sample`)**
   - Template for environment variables
   - Copy to `.env` and fill in required values

## Development Setup

1. **Prerequisites**:
   - Python 3.13+
   - uv (Python package manager)

2. **Installation**:

   ```bash
   uv sync
   ```

3. **Running the Bot**:

   ```bash
   uv run python main.py
   ```

## Maintenance Notes

- **Dependencies**: Managed via uv and `pyproject.toml`
- **Environment Variables**: Configured in `.env` (see `env.sample` for template)
- **Telegram Bot**: Requires API token in `.env` (set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHANNEL_ID`)

## Known Issues

- None currently documented

## Future Improvements

- Enhance error handling in Telegram notifications
- Add more comprehensive logging
- Expand test coverage

## Contact

- **Previous Maintainer**: [Prasetiyo Hadi]
- **Email**: [prasetiyohadi92@gmail.com]
