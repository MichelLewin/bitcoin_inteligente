import pandas as pd
from src.db.repository import Repository

class Consultas:
    def __init__(self):
        self.media_diaria = "vw_media_diaria"
        self.media_semanal = "vw_media_semanal"
        self.media_mensal = "vw_media_mensal"
        self.media_anual = "vw_media_anual"

    def evolucoes(self):
        repo = Repository()
        try:
            print("\n📊 Evolução diária:")
            df_diaria = repo.get_view(self.media_diaria)
            print(df_diaria.head())

            print("\n📊 Média semanal:")
            df_semanal = repo.get_view(self.media_semanal)
            print(df_semanal.head())

            print("\n📊 Média mensal:")
            df_mensal = repo.get_view(self.media_mensal)
            print(df_mensal.head())

            print("\n📊 Média anual:")
            df_anual = repo.get_view(self.media_anual)
            print(df_anual.head())

            return {
                "diaria": df_diaria,
                "semanal": df_semanal,
                "mensal": df_mensal,
                "anual": df_anual
            }
        except Exception as e:
            print(f"Erro ao obter evoluções: {type(e).__name__}: {str(e)}")
            return None