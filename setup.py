#!/usr/bin/env python3
"""
Monitoring System Setup Script
Helps configure environment variables for the monitoring system
"""

import os
import sys
from pathlib import Path


def print_header():
    print("=" * 60)
    print("🔧 MONITORING SYSTEM SETUP")
    print("=" * 60)
    print()


def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 40)


def get_user_input(prompt, default="", sensitive=False):
    """Get user input with optional default value"""
    if default:
        if sensitive:
            value = input(f"{prompt} [••••••••]: ").strip()
        else:
            value = input(f"{prompt} [{default}]: ").strip()
        return value if value else default
    else:
        while True:
            if sensitive:
                value = input(f"{prompt}: ").strip()
            else:
                value = input(f"{prompt}: ").strip()
            if value:
                return value
            print("❌ This field is required. Please enter a value.")


def create_env_file():
    """Create .env file with user configuration"""
    print_header()

    print("Welcome to the Monitoring System Setup!")
    print("This script will help you configure your environment variables.")
    print("Your sensitive information will be stored in a .env file (not committed to Git).")
    print()

    # Check if .env already exists
    env_path = Path(".env")
    if env_path.exists():
        overwrite = input(
            "⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return

    config = {}

    # Telegram Configuration
    print_section("TELEGRAM BOT SETUP")
    print("1. Go to https://t.me/BotFather")
    print("2. Create a new bot with /newbot command")
    print("3. Copy the bot token (starts with numbers, contains ':')")
    print()

    config['TELEGRAM_BOT_TOKEN'] = get_user_input(
        "Enter your Telegram bot token",
        sensitive=True
    )

    print("\n4. Message your bot from Telegram")
    print("5. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates")
    print("6. Find your chat ID in the JSON response")
    print()

    config['TELEGRAM_CHAT_ID'] = get_user_input(
        "Enter your Telegram chat ID"
    )

    # Email Configuration (Optional)
    print_section("EMAIL SETUP (Optional)")
    print("For Gmail: Enable 2FA, then get App Password from:")
    print("https://myaccount.google.com/apppasswords")
    print()

    setup_email = input("Set up email notifications? (y/N): ").strip().lower()
    if setup_email == 'y':
        config['EMAIL_SENDER'] = get_user_input(
            "Enter your Gmail address"
        )
        config['EMAIL_PASSWORD'] = get_user_input(
            "Enter your Gmail App Password (16 characters)",
            sensitive=True
        )
        config['EMAIL_RECEIVER'] = get_user_input(
            "Enter recipient email address",
            config['EMAIL_SENDER']
        )

    # Discord Configuration (Optional)
    print_section("DISCORD WEBHOOK (Optional)")
    print("1. Create Discord server: https://discord.com/")
    print("2. Right-click channel → Edit Channel → Integrations → Webhooks")
    print("3. Create webhook and copy URL")
    print()

    setup_discord = input(
        "Set up Discord notifications? (y/N): ").strip().lower()
    if setup_discord == 'y':
        config['DISCORD_WEBHOOK_URL'] = get_user_input(
            "Enter Discord webhook URL",
            sensitive=True
        )

    # API Keys (Optional)
    print_section("API KEYS (Optional)")
    print("Alpha Vantage API for real market data:")
    print("Get free key: https://www.alphavantage.co/support/#api-key")
    print()

    setup_api = input("Set up Alpha Vantage API key? (y/N): ").strip().lower()
    if setup_api == 'y':
        config['ALPHA_VANTAGE_API_KEY'] = get_user_input(
            "Enter Alpha Vantage API key",
            sensitive=True
        )

    # Alert Thresholds
    print_section("ALERT THRESHOLDS")
    print("Customize when you want to receive alerts:")
    print()

    config['BITCOIN_ALERT_THRESHOLD'] = get_user_input(
        "Bitcoin alert threshold (INR)",
        "5000000"
    )

    config['NIFTY_DROP_THRESHOLD'] = get_user_input(
        "NIFTY drop alert threshold (%)",
        "-1.5"
    )

    config['INFLATION_CRITICAL_THRESHOLD'] = get_user_input(
        "Inflation critical threshold (%)",
        "6.0"
    )

    config['GOLD_HIGH_THRESHOLD'] = get_user_input(
        "Gold high alert threshold (INR per gram)",
        "7500"
    )

    config['SILVER_HIGH_THRESHOLD'] = get_user_input(
        "Silver high alert threshold (INR per gram)",
        "100"
    )

    # Schedule Configuration
    print_section("SCHEDULE CONFIGURATION")
    config['MONITORING_TIME'] = get_user_input(
        "Daily monitoring time (HH:MM)",
        "09:00"
    )

    config['EMAIL_REPORT_TIME'] = get_user_input(
        "Daily email report time (HH:MM)",
        "18:00"
    )

    # Write .env file
    print_section("CREATING CONFIGURATION")
    try:
        with open('.env', 'w') as f:
            f.write("# Environment Variables for Monitoring System\n")
            f.write("# Generated by setup.py - DO NOT commit to GitHub\n\n")

            for key, value in config.items():
                if 'PASSWORD' in key or 'TOKEN' in key or 'KEY' in key or 'SECRET' in key:
                    f.write(f"{key}={value}\n")
                else:
                    f.write(f"{key}={value}\n")

        print("✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")

        # Set file permissions (restrictive)
        try:
            os.chmod('.env', 0o600)  # Owner read/write only
            print("🔒 File permissions set to restrictive (owner only)")
        except:
            pass  # Windows might not support this

    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

    # Test configuration
    print_section("TESTING CONFIGURATION")
    print("Testing your configuration...")

    # Test Telegram
    if 'TELEGRAM_BOT_TOKEN' in config and 'TELEGRAM_CHAT_ID' in config:
        try:
            import requests
            token = config['TELEGRAM_BOT_TOKEN']
            chat_id = config['TELEGRAM_CHAT_ID']
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            response = requests.post(url, data={
                'chat_id': chat_id,
                'text': '🧪 Test message from Monitoring System Setup'
            }, timeout=10)

            if response.status_code == 200:
                print("✅ Telegram: Test message sent successfully")
            else:
                print(
                    f"⚠️  Telegram: API responded with status {response.status_code}")
        except Exception as e:
            print(f"⚠️  Telegram: Test failed - {e}")

    # Test Email (if configured)
    if 'EMAIL_SENDER' in config and 'EMAIL_PASSWORD' in config:
        try:
            import smtplib
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(config['EMAIL_SENDER'], config['EMAIL_PASSWORD'])
            server.quit()
            print("✅ Email: Authentication successful")
        except Exception as e:
            print(f"⚠️  Email: Authentication failed - {e}")

    print_section("SETUP COMPLETE")
    print("🎉 Your monitoring system is configured!")
    print()
    print("Next steps:")
    print("1. Run: python main.py (test once)")
    print("2. Run: python scheduler.py (daily automation)")
    print("3. Check Telegram for alerts")
    print("4. Check email for daily reports")
    print()
    print("⚠️  Remember: Never commit .env file to GitHub!")
    print("   It's already in .gitignore for your safety.")


if __name__ == "__main__":
    create_env_file()
