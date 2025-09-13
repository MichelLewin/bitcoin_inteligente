from src.api.coingecko_client import CoinGeckoClient
from src.db.repository import Repository

def main():
    client = CoinGeckoClient()
    # ajuste 'days' conforme necessidade (ex: 30, 90, 'max')
    df = client.get_bitcoin_market_chart(days=30)
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
    main()
