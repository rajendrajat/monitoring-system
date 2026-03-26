import sys
import traceback
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("[DEBUG] Starting imports...")

try:
    print("[DEBUG] Importing collectors.crypto...")
    from collectors.crypto import get_crypto_price
    print("[DEBUG] ✓ collectors.crypto imported")

    print("[DEBUG] Importing collectors.market...")
    from collectors.market import get_market_data
    print("[DEBUG] ✓ collectors.market imported")

    print("[DEBUG] Importing collectors.news...")
    from collectors.news import get_news
    print("[DEBUG] ✓ collectors.news imported")

    print("[DEBUG] Importing collectors.inflation...")
    from collectors.inflation import get_inflation_rate
    print("[DEBUG] ✓ collectors.inflation imported")

    print("[DEBUG] Importing collectors.metals...")
    from collectors.metals import get_metals_prices
    print("[DEBUG] ✓ collectors.metals imported")

    print("[DEBUG] Importing rules.engine...")
    from rules.engine import evaluate_rules
    print("[DEBUG] ✓ rules.engine imported")

    print("[DEBUG] All imports successful!\n")
except ImportError as e:
    print(f"[FATAL] Import error: {e}")
    traceback.print_exc()
    sys.exit(1)


def main():
    print("Fetching data...")

    data = {
        "crypto": get_crypto_price(),
        "market": get_market_data(),
        "news": get_news(),
        "inflation": get_inflation_rate(),
        "metals": get_metals_prices()
    }

    # Display fetched data
    print("\n📊 Collected Data:")
    if data.get("crypto"):
        print(f"  💰 Crypto: {data['crypto']}")
    else:
        print("  💰 Crypto: No data")

    if data.get("market"):
        print(f"  📈 Market: {data['market']}")
    else:
        print("  📈 Market: No data")

    if data.get("news"):
        print(f"  📰 News: {len(data['news'])} LATEST headlines fetched")
        # Show first 5 headlines with dates
        for i, item in enumerate(data['news'][:5], 1):
            if isinstance(item, dict):
                headline = item.get("title", "")
                date = item.get("date", "")
                if date:
                    print(f"    {i}. {headline}")
                    print(f"       [{date}]")
                else:
                    print(f"    {i}. {headline}")
            else:
                # Fallback for old format
                print(f"    {i}. {item}")
    else:
        print("  📰 News: No data")

    if data.get("inflation"):
        inf = data['inflation']
        print(
            f"  📊 India Inflation (Current): {inf['current_rate']}% (Expected: {inf['expected_rate']}%, RBI Target: {inf['rbi_target']}%)")
        print(
            f"      Trend: {inf['trend'].capitalize()} | Status: {inf['status'].replace('_', ' ').title()}")
    else:
        print("  📊 Inflation: No data")

    if data.get("metals"):
        metals = data['metals']
        gold_price = metals.get('gold', {}).get('price_inr', 'N/A')
        silver_price = metals.get('silver', {}).get('price_inr', 'N/A')
        print(
            f"  🥇 Gold: ₹{gold_price:.2f}/gram | 🥈 Silver: ₹{silver_price:.2f}/gram")
    else:
        print("  🥇 Precious Metals: No data")

    print("\nEvaluating rules...")
    evaluate_rules(data)

    print("\n✅ Monitoring cycle complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[FATAL] Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
