from collectors.crypto import get_crypto_price
from collectors.market import get_market_data
from collectors.news import get_news
from rules.engine import evaluate_rules


def main():
    print("Fetching data...")

    data = {
        "crypto": get_crypto_price(),
        "market": get_market_data(),
        "news": get_news()
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
        print(f"  📰 News: {len(data['news'])} headlines fetched")
        # Show first 3 headlines
        for i, headline in enumerate(data['news'][:3], 1):
            print(f"    {i}. {headline}")
    else:
        print("  📰 News: No data")

    print("\nEvaluating rules...")
    evaluate_rules(data)

    print("\n✅ Monitoring cycle complete!")


if __name__ == "__main__":
    main()
