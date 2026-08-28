from app.extractor import get_crypto_prices, get_usd_kes_rate
from app.transformer import transform_prices
from app.loader import load_to_postgres


def main():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

    usd_prices = get_crypto_prices(symbols)
    usd_kes_rate = get_usd_kes_rate()

    records = transform_prices(usd_prices, usd_kes_rate)

    load_to_postgres(records)

    print("\n=== Crypto Price Report (KES) ===")
    print(f"{'Symbol':<12}{'USD Price':>15}{'KES Price':>18}")
    print("-" * 45)
    for r in records:
        print(f"{r['symbol']:<12}{r['usd_price']:>15,.2f}{r['ksh_price']:>18,.2f}")
    print()


if __name__ == "__main__":
    main()