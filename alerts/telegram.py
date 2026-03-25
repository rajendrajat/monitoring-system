import requests

BOT_TOKEN = "USE_YOUR_TELEGRAM_TOKEN"
CHAT_ID = "USE_YOUR_CHAT_ID"  # Your numeric chat ID


def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(url, data=payload, timeout=10)

    except Exception as e:
        print(f"[ALERT ERROR] {e}")
