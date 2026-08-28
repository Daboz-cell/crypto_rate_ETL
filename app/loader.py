import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Loads DB credentials from .env.

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def load_to_postgres(records):
   """
    Writes price records into the crypto_rates table.

   """
   with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS crypto_rates (
                id SERIAL PRIMARY KEY,
                symbol TEXT NOT NULL,
                usd_price NUMERIC NOT NULL,
                ksh_price NUMERIC NOT NULL,
                fetched_at TIMESTAMP DEFAULT NOW()
            )
        """))
        for r in records:
            conn.execute(
                text("""
                    INSERT INTO crypto_rates (symbol, usd_price, ksh_price)
                    VALUES (:symbol, :usd_price, :ksh_price)
                """),
                {"symbol": r["symbol"], "usd_price": r["usd_price"], "ksh_price": r["ksh_price"]},
                
            )
        conn.commit()
        