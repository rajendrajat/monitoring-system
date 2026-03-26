import requests
import json
import os

# Discord Webhook Configuration
# Get your webhook URL from: https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL", "YOUR_DISCORD_WEBHOOK_URL")


def send_discord_alert(message, embed=None):
    """
    Send alert via Discord Webhook

    Args:
        message (str): Simple text message
        embed (dict): Optional Discord embed object for rich formatting

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL":
        print(
            "[DISCORD] Webhook URL not configured. See alerts/discord.py for setup instructions")
        return False

    try:
        # Prepare payload
        if embed:
            payload = {
                "username": "📊 Monitoring Bot",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/822/822143.png",
                "embeds": [embed]
            }
        else:
            payload = {
                "username": "📊 Monitoring Bot",
                "content": message,
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/822/822143.png"
            }

        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            timeout=10
        )

        if response.status_code == 204:
            print(f"[DISCORD] ✅ Alert sent successfully")
            return True
        else:
            print(f"[DISCORD] Error: Status {response.status_code}")
            return False

    except Exception as e:
        print(f"[DISCORD ERROR] {e}")
        return False


def send_discord_embed(title, description, fields=None, color=3447003):
    """
    Send formatted message via Discord embed

    Args:
        title (str): Embed title
        description (str): Embed description
        fields (list): List of {"name": "...", "value": "..."} dicts
        color (int): Decimal color code (default blue)

    Returns:
        bool: Success status
    """
    embed = {
        "title": title,
        "description": description,
        "color": color
    }

    if fields:
        embed["fields"] = fields

    return send_discord_alert(None, embed)


def send_discord_news_alert(headlines):
    """Send news headlines to Discord"""
    if not headlines:
        return False

    fields = []
    for i, item in enumerate(headlines[:5], 1):
        if isinstance(item, dict):
            title = item.get("title", "")
            date = item.get("date", "")
        else:
            title = item
            date = ""

        fields.append({
            "name": f"📰 {i}. {title[:100]}...",
            "value": f"*{date}*" if date else "Recent",
            "inline": False
        })

    return send_discord_embed(
        title="🔔 Breaking News Alert",
        description=f"Found {len(headlines)} relevant headlines",
        fields=fields,
        color=15105570  # Orange
    )


# Setup Instructions:
# 1. Create a Discord server: https://discord.com/
# 2. Create a text channel for alerts
# 3. Right-click channel → Edit Channel → Integrations → Webhooks
# 4. Create Webhook and copy URL
# 5. Paste URL as DISCORD_WEBHOOK_URL above
