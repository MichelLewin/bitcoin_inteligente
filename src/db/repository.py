from sqlalchemy import create_engine, text
from src.config import DB_CONFIG
import pandas as pd

class Repository:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )

    def save_dataframe(self, df, table_name="bitcoin_prices"):
        df.to_sql(table_name, self.engine, if_exists="replace", index=False)

    def get_count(self, table_name="bitcoin_prices"):
        query = text(f"SELECT COUNT(*) FROM {table_name}")
        with self.engine.connect() as conn:
            result = conn.execute(query).scalar()
        return result
    
    def get_view(self, view_name):
        """Retorna um DataFrame a partir de uma view no Postgres"""
        query = f"SELECT * FROM {view_name}"
        return pd.read_sql(query, self.engine)