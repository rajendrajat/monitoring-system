import requests
import time
import os

# Load environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

# Track sent messages to avoid duplicates
sent_messages = set()


def send_telegram_alert(message, retry_count=3):
    """
    Send alert via Telegram with retry mechanism and error handling

    Args:
        message (str): Alert message to send
        retry_count (int): Number of retries on failure

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Avoid duplicate messages within same cycle
        msg_hash = hash(message)
        if msg_hash in sent_messages:
            print(
                f"[TELEGRAM] Message already sent (duplicate): {message[:50]}...")
            return True

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"  # Allow basic HTML formatting
        }

        for attempt in range(retry_count):
            try:
                response = requests.post(url, data=payload, timeout=10)
                response.raise_for_status()  # Raise exception for bad status codes

                if response.status_code == 200:
                    sent_messages.add(msg_hash)
                    print(
                        f"[TELEGRAM] ✅ Alert sent successfully: {message[:50]}...")
                    return True
                else:
                    print(
                        f"[TELEGRAM] Unexpected status {response.status_code}: {response.text}")

            except requests.exceptions.Timeout:
                print(
                    f"[TELEGRAM] Timeout on attempt {attempt + 1}/{retry_count}")
                if attempt < retry_count - 1:
                    time.sleep(2)  # Wait before retry
                    continue
                raise

            except requests.exceptions.RequestException as e:
                print(
                    f"[TELEGRAM] Request error on attempt {attempt + 1}/{retry_count}: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2)  # Wait before retry
                    continue
                raise

        return False

    except Exception as e:
        print(f"[TELEGRAM ERROR] Failed to send alert: {e}")
        print(f"[TELEGRAM INFO] Please verify:")
        print(f"  - Bot token is set in .env file")
        print(f"  - Chat ID is set in .env file")
        print(f"  - Internet connection is active")
        print(f"  - Bot token format: starts with number, contains ':'")
        return False


def send_telegram_notification(title, message):
    """
    Send formatted notification with title and message

    Args:
        title (str): Alert title
        message (str): Alert details
    """
    formatted_msg = f"<b>{title}</b>\n{message}"
    return send_telegram_alert(formatted_msg)
