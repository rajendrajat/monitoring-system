from alerts.telegram import send_telegram_alert


def evaluate_rules(data):
    alerts = []

    crypto = data.get("crypto")
    market = data.get("market")
    news = data.get("news")

    print("\n🔍 Evaluating Rules:")

    # 🔹 Rule 1: Crypto crash
    if crypto:
        btc_price = crypto.get("bitcoin")
        print(
            f"  Rule 1 - Bitcoin price: ₹{btc_price} (alert if < ₹50,00,000)")
        if btc_price and btc_price < 5000000:
            alerts.append(f"🚨 Bitcoin dropped below 50L: ₹{btc_price}")
    else:
        print("  Rule 1 - Crypto data not available")

    # 🔹 Rule 2: Market crash
    if market:
        nifty = market.get("^NSEI", {})
        change = nifty.get("change_percent", 0)
        print(f"  Rule 2 - NIFTY change: {change:.2f}% (alert if < -1.5%)")
        if change < -1.5:
            alerts.append(f"📉 NIFTY down {change:.2f}%")
    else:
        print("  Rule 2 - Market data not available")

    # 🔹 Rule 3: News keyword alert
    if news:
        print(
            f"  Rule 3 - Checking {len(news)} news headlines for keywords: war, iran, oil, inflation")
        for headline in news:
            if any(word in headline.lower() for word in ["war", "iran", "oil", "inflation"]):
                alerts.append(f"📰 Important News: {headline}")
    else:
        print("  Rule 3 - News data not available")

    # 🔹 Send alerts
    if alerts:
        print(f"\n🚨 {len(alerts)} alert(s) triggered:")
        for alert in alerts:
            print(f"  {alert}")
            send_telegram_alert(alert)
    else:
        print("\n✅ No alerts triggered this cycle")
