from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# Logging setup
import logging
from copy import copy
from pythonjsonlogger.json import JsonFormatter

# Server setup
import uvicorn

app = FastAPI()

# Environment variables (best practice for security)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

# Fallback to loading from .env file if environment variables are not set
if not BOT_TOKEN or not CHANNEL_ID:
    from dotenv import load_dotenv

    load_dotenv()
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID must be set as environment variables or in a .env file."
    )

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.get("/")
async def read_root():
    return {"message": "Hello from godevopsid-bot!"}


def send_telegram_message(message):
    """Sends a message to the Telegram channel using the bot."""
    try:
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message,
            "parse_mode": "Markdown",  # Optional:  Use Markdown formatting
        }
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print("Telegram message sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return False


class TelegramRequest(BaseModel):
    message: str


@app.post("/")
def notification_endpoint(request: TelegramRequest):
    """
    Handles HTTP requests and sends a Telegram notification.
    Expects a JSON payload with a "message" key in a POST request,
    or a "message" query parameter in a GET request.
    """

    if send_telegram_message(request.message):
        return {"status": "success", "message": "Notification sent to Telegram"}
    else:
        return {"status": "error", "message": "Failed to send notification"}


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


# Logging configuration
# Reference: https://github.com/encode/uvicorn/discussions/2027


class UvicornJSONAccessFormatter(JsonFormatter):
    def format(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        client_addr, method, full_path, http_version, status_code = recordcopy.args  # type: ignore[misc]
        recordcopy.__dict__.update(
            {
                "client_addr": client_addr,
                "method": method,
                "full_path": full_path,
                "http_version": http_version,
                "status_code": status_code,
            }
        )
        return super().format(record=recordcopy)


class UvicornJSONDefaultFormatter(JsonFormatter):
    def format(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        recordcopy.__dict__.pop("color_message", None)
        return super().format(record=recordcopy)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": UvicornJSONDefaultFormatter,
        },
        "access": {
            "()": UvicornJSONAccessFormatter,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}

# Server startup
if __name__ == "__main__":
    uvicorn.run(
        app,
        # Get the host from the environment variable or use localhost as default
        host=os.environ.get("HOST", "localhost"),
        # Get the port from the environment variable or use 5000 as default
        port=int(os.environ.get("PORT", 5000)),
        log_config=LOGGING_CONFIG,
    )
