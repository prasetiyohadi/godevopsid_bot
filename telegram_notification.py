from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

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
    raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID must be set as environment variables or in a .env file.")


TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_message(message):
    """Sends a message to the Telegram channel using the bot."""
    try:
        payload = {
            "chat_id": CHANNEL_ID,
            "text": message,
            "parse_mode": "Markdown"  # Optional:  Use Markdown formatting
        }
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print("Telegram message sent successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return False

@app.route("/", methods=["POST", "GET"])  # Allow both POST and GET
def notification_endpoint():
    """
    Handles HTTP requests and sends a Telegram notification.
    Expects a JSON payload with a "message" key in a POST request,
    or a "message" query parameter in a GET request.
    """

    if request.method == "POST":
        try:
            data = request.get_json()
            message = data.get("message")
            if not message:
                return jsonify({"error": "Missing 'message' in JSON payload"}), 400
        except Exception as e:
            return jsonify({"error": f"Invalid JSON payload: {e}"}), 400

    elif request.method == "GET":
        message = request.args.get("message")
        if not message:
            return jsonify({"error": "Missing 'message' query parameter"}), 400

    else:
        return jsonify({"error": "Method not allowed"}), 405


    if send_telegram_message(message):
        return jsonify({"status": "success", "message": "Notification sent to Telegram"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send notification"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Get the port from the environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) # Make sure to set debug=False in production
