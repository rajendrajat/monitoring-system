import requests


def get_crypto_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "inr"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        return {
            "bitcoin": data["bitcoin"]["inr"],
            "ethereum": data["ethereum"]["inr"]
        }

    except Exception as e:
        print(f"[CRYPTO ERROR] {e}")
        return None
