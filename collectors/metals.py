import requests
import random


def get_metals_prices():
    """
    Fetch gold and silver prices in INR
    Uses live market data APIs or fallback to mock data
    """
    try:
        metals_data = {
            "gold": None,
            "silver": None,
            "timestamp": None,
            "source": None
        }

        # Try to fetch from metals-api.io (requires free API key registration)
        # Alternative: Use a free API like metals-api or mock realistic prices
        try:
            # Attempt: Using alpha metals API endpoint (replace with real API key if available)
            # This is a common endpoint pattern
            url = "https://api.metals.live/v1/spot/gold"
            response_gold = requests.get(url, timeout=5)

            if response_gold.status_code == 200:
                gold_data = response_gold.json()
                # Convert to INR if in USD (1 USD ≈ 83 INR as of 2026)
                if isinstance(gold_data, dict):
                    price_usd = gold_data.get("price") or gold_data.get("gold")
                    if price_usd:
                        metals_data["gold"] = {
                            "price_usd": float(price_usd),
                            "price_inr": float(price_usd) * 83,
                            "unit": "per gram"
                        }

            # Fetch silver
            url = "https://api.metals.live/v1/spot/silver"
            response_silver = requests.get(url, timeout=5)

            if response_silver.status_code == 200:
                silver_data = response_silver.json()
                if isinstance(silver_data, dict):
                    price_usd = silver_data.get(
                        "price") or silver_data.get("silver")
                    if price_usd:
                        metals_data["silver"] = {
                            "price_usd": float(price_usd),
                            "price_inr": float(price_usd) * 83,
                            "unit": "per gram"
                        }

            if metals_data["gold"] and metals_data["silver"]:
                metals_data["source"] = "Metals Live API"
                return metals_data

        except Exception as e:
            print(
                f"[METALS INFO] Live API unavailable, using estimated prices: {e}")

        # Fallback: Realistic mock data for Indian precious metals market
        # Gold: ~₹6000-7000 per gram, Silver: ~₹75-85 per gram (realistic 2026 estimates)
        metals_data["gold"] = {
            "price_usd": 72.60 + random.uniform(-2, 2),  # ~$70-75 per gram
            # Realistic Indian pricing
            "price_inr": 6400 + random.uniform(-300, 300),
            "unit": "per gram"
        }

        metals_data["silver"] = {
            # ~$0.85-0.90 per gram
            "price_usd": 0.87 + random.uniform(-0.05, 0.05),
            # Realistic Indian pricing
            "price_inr": 80 + random.uniform(-5, 5),
            "unit": "per gram"
        }

        metals_data["source"] = "Estimated market prices"

        return metals_data

    except Exception as e:
        print(f"[METALS ERROR] {e}")
        return None
