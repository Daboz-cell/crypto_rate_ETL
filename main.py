import argparse
from app.extractor import get_crypto_prices, get_usd_kes_rate
from app.transformer import transform_prices
from app.loader import load_to_postgres


def main():
    # Create a parser object that will read arguments typed on the command line
    parser = argparse.ArgumentParser()
    # Register a required --symbol flag
    parser.add_argument("--symbol", required=True, help="Comma-separated Binance symbols, e.g. BTCUSDT,ETHUSDT")
    # Read the actual command-line input and store it as a Namespace object
    args = parser.parse_args()
    #Split into a list of separate symbols
    symbols = args.symbol.split(",")

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