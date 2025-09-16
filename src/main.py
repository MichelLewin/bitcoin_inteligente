from src.api.coingecko_client import CoinGeckoClient
from src.db.repository import Repository

class BitcoinDataCollector:
    def __init__(self):
        self.days = 365

    def main(self):
        client = CoinGeckoClient()
        df = client.get_bitcoin_market_chart(self.days)
        print(f"Coletado: {len(df)} registros")

        repo = Repository()
        repo.save_dataframe(df)
        print("Dados salvos no banco.")

        try:
            total = repo.get_count()
            print(f"Total de registros na tabela: {total}")
        except Exception as e:
            print('Erro ao consultar contagem:', e)

if __name__ == "__main__":
    collector = BitcoinDataCollector()  # Cria uma instância da classe
    collector.main()  # Chama o método main a partir da instância
