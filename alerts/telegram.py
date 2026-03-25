import requests

BOT_TOKEN = "8651643159:AAEGAuw5SZkf2ruaeKr26zbd5Bv_nbjlA-4"
CHAT_ID = "7230210433"  # Your numeric chat ID


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
