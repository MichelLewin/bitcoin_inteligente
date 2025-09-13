import unittest
from src.api.coingecko_client import CoinGeckoClient

class TestCoinGeckoClient(unittest.TestCase):
    def test_get_bitcoin_market_chart(self):
        client = CoinGeckoClient()
        df = client.get_bitcoin_market_chart(days=1)
        self.assertGreater(len(df), 0)

if __name__ == "__main__":
    unittest.main()
