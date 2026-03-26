from alerts.telegram import send_telegram_alert
import os


def evaluate_rules(data):
    alerts = []

    crypto = data.get("crypto")
    market = data.get("market")
    news = data.get("news")
    inflation = data.get("inflation")
    metals = data.get("metals")

    print("\n🔍 Evaluating Rules:")

    # 🔹 Rule 1: Crypto crash
    if crypto:
        btc_price = crypto.get("bitcoin")
        btc_threshold = int(os.getenv("BITCOIN_ALERT_THRESHOLD", "5000000"))
        print(
            f"  Rule 1 - Bitcoin price: ₹{btc_price} (alert if < ₹{btc_threshold:,})")
        if btc_price and btc_price < btc_threshold:
            alerts.append(
                f"🚨 Bitcoin dropped below {btc_threshold:,}: ₹{btc_price}")
    else:
        print("  Rule 1 - Crypto data not available")

    # 🔹 Rule 2: Market crash
    if market:
        nifty = market.get("^NSEI", {})
        change = nifty.get("change_percent", 0)
        nifty_threshold = float(os.getenv("NIFTY_DROP_THRESHOLD", "-1.5"))
        print(
            f"  Rule 2 - NIFTY change: {change:.2f}% (alert if < {nifty_threshold:.1f}%)")
        if change < nifty_threshold:
            alerts.append(f"📉 NIFTY down {change:.2f}%")
    else:
        print("  Rule 2 - Market data not available")

    # 🔹 Rule 3: News keyword alert (FRESH NEWS)
    if news:
        print(
            f"  Rule 3 - Checking {len(news)} LATEST news headlines for keywords: war, iran, oil, inflation, gold, silver, inflation")

        breaking_news_count = 0
        for item in news:
            # Handle both old format (string) and new format (dict)
            if isinstance(item, dict):
                headline = item.get("title", "")
                pub_date = item.get("date", "")
            else:
                headline = item
                pub_date = ""

            if any(word in headline.lower() for word in ["war", "iran", "oil", "inflation", "gold", "silver"]):
                breaking_news_count += 1
                # Format with date info if available
                if pub_date:
                    news_alert = f"📰 BREAKING: {headline}\n[{pub_date}]"
                else:
                    news_alert = f"📰 BREAKING: {headline}"

                alerts.append(news_alert)

        if breaking_news_count > 0:
            print(f"     Found {breaking_news_count} breaking news items")
    else:
        print("  Rule 3 - News data not available")

    # 🔹 Rule 4: Inflation alert
    if inflation:
        current_inf = inflation.get("current_rate")
        target_inf = inflation.get("rbi_target", 4.0)
        critical_threshold = float(
            os.getenv("INFLATION_CRITICAL_THRESHOLD", "6.0"))
        print(
            f"  Rule 4 - Inflation Rate: {current_inf}% (RBI target: {target_inf}%, alert if > {critical_threshold}%)")
        if current_inf and current_inf > critical_threshold:
            alerts.append(
                f"⚠️ ALERT: Inflation above {critical_threshold}%: Current {current_inf}%")
        elif current_inf and current_inf > target_inf + 1.5:
            alerts.append(
                f"📊 High Inflation: {current_inf}% (above RBI target of {target_inf}%)")
    else:
        print("  Rule 4 - Inflation data not available")

    # 🔹 Rule 5: Precious metals price alert
    if metals:
        gold_price = metals.get('gold', {}).get('price_inr')
        silver_price = metals.get('silver', {}).get('price_inr')
        gold_threshold = int(os.getenv("GOLD_HIGH_THRESHOLD", "7500"))
        silver_threshold = int(os.getenv("SILVER_HIGH_THRESHOLD", "100"))
        print(
            f"  Rule 5 - Gold: ₹{gold_price:.2f}/g, Silver: ₹{silver_price:.2f}/g (alert if gold > ₹{gold_threshold}/g)")

        if gold_price and gold_price > gold_threshold:
            alerts.append(
                f"🚨 Gold Price High: ₹{gold_price:.2f}/gram (above ₹{gold_threshold})")
        elif gold_price and gold_price > gold_threshold - 300:  # Warning at 300 below threshold
            alerts.append(f"🥇 Gold Price Notice: ₹{gold_price:.2f}/gram")

        if silver_price and silver_price > silver_threshold:
            alerts.append(f"🥈 Silver Price Alert: ₹{silver_price:.2f}/gram")
    else:
        print("  Rule 5 - Precious metals data not available")

    # 🔹 Send alerts via Telegram
    if alerts:
        print(f"\n🚨 {len(alerts)} alert(s) triggered:")
        for alert in alerts:
            print(f"  {alert}")
            # Send each alert to Telegram
            success = send_telegram_alert(alert)
            if not success:
                print(f"  ⚠️ Failed to send alert to Telegram")

        # Also send summary alert
        summary = f"📊 News Alert Summary: {len(alerts)} items detected\n"
        for i, alert in enumerate(alerts[:5], 1):  # Show first 5 in summary
            summary += f"{i}. {alert[:80]}...\n" if len(
                alert) > 80 else f"{i}. {alert}\n"

        send_telegram_alert(summary)
    else:
        print("\n✅ No alerts triggered this cycle")
