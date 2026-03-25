import requests
import random


def get_market_data():
    try:
        # Try Alpha Vantage first (requires free API key from https://www.alphavantage.co/support/#api-key)
        api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your API key

        if api_key != "YOUR_ALPHA_VANTAGE_API_KEY":  # Only try if user has set an API key
            symbols = ["NSEI", "BSESN"]
            results = {}

            for symbol in symbols:
                url = f"https://www.alphavantage.co/query"
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": api_key
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if "Global Quote" in data:
                        quote = data["Global Quote"]
                        results[symbol] = {
                            "price": float(quote.get("05. price", 0)),
                            "change_percent": float(quote.get("10. change percent", "0%").strip("%"))
                        }

            if results:
                return results

        # Fallback: Return mock data for testing
        print(
            "[MARKET INFO] Using mock market data (set Alpha Vantage API key for real data)")
        return {
            "^NSEI": {
                "price": 22000 + random.uniform(-500, 500),
                "change_percent": random.uniform(-2, 2)
            },
            "^BSESN": {
                "price": 72000 + random.uniform(-1000, 1000),
                "change_percent": random.uniform(-2, 2)
            }
        }

    except Exception as e:
        print(f"[MARKET ERROR] {e}")
        return None
