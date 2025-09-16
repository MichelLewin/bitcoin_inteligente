import requests
import pandas as pd

class CoinGeckoClient:
    def __init__(self):
        self.BASE_URL = "https://api.coingecko.com/api/v3"

    def get_bitcoin_market_chart(self, days, vs_currency="usd"):
        """
        Retorna DataFrame com colunas: timestamp (datetime) e price (float).
        days: número de dias para recuperar (aceita 'max' também).
        """
        url = f"{self.BASE_URL}/coins/bitcoin/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        prices = data.get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
