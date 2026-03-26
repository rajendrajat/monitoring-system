import sys
import traceback
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("[DEBUG] Starting scheduler imports...")

try:
    from collectors.crypto import get_crypto_price
    from collectors.market import get_market_data
    from collectors.news import get_news
    from collectors.inflation import get_inflation_rate
    from collectors.metals import get_metals_prices
    from rules.engine import evaluate_rules
    from alerts.telegram import send_telegram_alert
    from alerts.email import send_daily_report
    print("[DEBUG] ✓ All modules imported successfully")
except ImportError as e:
    print(f"[FATAL] Import error: {e}")
    traceback.print_exc()
    sys.exit(1)


def run_monitoring_cycle():
    """Execute one complete monitoring cycle"""
    try:
        print(f"\n{'='*80}")
        print(
            f"🔄 Monitoring Cycle Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

        print("\nFetching data...")

        data = {
            "crypto": get_crypto_price(),
            "market": get_market_data(),
            "news": get_news(),
            "inflation": get_inflation_rate(),
            "metals": get_metals_prices()
        }

        # Display summary
        print("\n📊 Collected Data Summary:")
        if data.get("crypto"):
            print(f"  ✅ Crypto: {list(data['crypto'].keys())}")
        if data.get("market"):
            print(f"  ✅ Market: {list(data['market'].keys())}")
        if data.get("news"):
            print(f"  ✅ News: {len(data['news'])} headlines")
        if data.get("inflation"):
            print(f"  ✅ Inflation: {data['inflation']['current_rate']}%")
        if data.get("metals"):
            print(
                f"  ✅ Metals: Gold ₹{data['metals']['gold']['price_inr']:.2f}/g")

        # Evaluate rules and get alerts
        alerts = []
        evaluate_rules(data)  # This handles Telegram alerts automatically

        # Count alerts from console output (they're sent in evaluate_rules)
        print(
            f"\n✅ Monitoring cycle completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")

        return data, alerts

    except Exception as e:
        error_msg = f"[MONITORING ERROR] {e}"
        print(f"\n{error_msg}")
        traceback.print_exc()
        send_telegram_alert(f"❌ {error_msg}")
        return None, []


def send_daily_email_report():
    """Send daily email report with monitoring data"""
    try:
        print(
            f"\n📧 Preparing daily email report: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Fetch current data for report
        data = {
            "crypto": get_crypto_price(),
            "market": get_market_data(),
            "news": get_news(),
            "inflation": get_inflation_rate(),
            "metals": get_metals_prices()
        }

        # Get alerts (but don't send - we just want them for the report)
        # We'll collect them separately for the report
        alerts = []

        # Send email report
        success = send_daily_report(data, alerts)

        if success:
            print(f"✅ Daily email report sent successfully")
            send_telegram_alert(
                f"📧 Daily email report sent at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"⚠️ Failed to send daily email report")

    except Exception as e:
        error_msg = f"[EMAIL REPORT ERROR] {e}"
        print(f"\n{error_msg}")
        traceback.print_exc()
        send_telegram_alert(error_msg)


def start_scheduler(
    monitoring_hour=9,
    monitoring_minute=0,
    email_hour=18,
    email_minute=0
):
    """
    Start the APScheduler with monitoring and email tasks

    Args:
        monitoring_hour (int): Hour for monitoring cycle (24-hour format)
        monitoring_minute (int): Minute for monitoring cycle
        email_hour (int): Hour for daily email report (24-hour format)
        email_minute (int): Minute for daily email report
    """
    try:
        scheduler = BackgroundScheduler()

        # Schedule monitoring cycle (daily at specified time)
        scheduler.add_job(
            run_monitoring_cycle,
            CronTrigger(hour=monitoring_hour, minute=monitoring_minute),
            id="daily_monitoring",
            name="Daily Monitoring Cycle",
            replace_existing=True
        )
        print(
            f"✅ Scheduled monitoring cycle daily at {monitoring_hour:02d}:{monitoring_minute:02d}")

        # Schedule daily email report
        scheduler.add_job(
            send_daily_email_report,
            CronTrigger(hour=email_hour, minute=email_minute),
            id="daily_email_report",
            name="Daily Email Report",
            replace_existing=True
        )
        print(
            f"✅ Scheduled daily email report at {email_hour:02d}:{email_minute:02d}")

        # Start scheduler
        scheduler.start()
        print(f"\n🚀 Scheduler started successfully!")
        print(
            f"⏰ Next monitoring: Tomorrow at {monitoring_hour:02d}:{monitoring_minute:02d}")
        print(
            f"📧 Next email report: Today/Tomorrow at {email_hour:02d}:{email_minute:02d}")

        return scheduler

    except Exception as e:
        print(f"\n[SCHEDULER ERROR] {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("[INFO] Starting Monitoring System with Auto-Scheduler")
    print("[INFO] The scheduler will run in the background")
    print("[INFO] Press Ctrl+C to stop\n")

    # Configuration (customize these times)
    # Daily monitoring at 9 AM
    MONITORING_TIME = os.getenv("MONITORING_TIME", "09:00")
    # Daily email report at 6 PM
    EMAIL_TIME = os.getenv("EMAIL_REPORT_TIME", "18:00")

    monitoring_hour = int(MONITORING_TIME.split(":")[0])
    monitoring_minute = int(MONITORING_TIME.split(":")[1])
    email_hour = int(EMAIL_TIME.split(":")[0])
    email_minute = int(EMAIL_TIME.split(":")[1])

    scheduler = start_scheduler(
        monitoring_hour, monitoring_minute, email_hour, email_minute)

    try:
        # Keep scheduler running
        print("\n📌 Scheduler is running. Press Ctrl+C to stop.\n")
        while True:
            pass
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down scheduler...")
        scheduler.shutdown()
        print("✅ Scheduler stopped cleanly")
