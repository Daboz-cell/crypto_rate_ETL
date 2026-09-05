# Crypto Rate ETL

A small, containerized Python ETL application that extracts live cryptocurrency prices from the Binance Spot API, extracts the current USD/KES exchange rate from the Frankfurter API, converts the crypto price into Kenyan Shillings, stores the results in PostgreSQL, and prints a clean report to the terminal.

## Features

- Fetches live spot prices for multiple crypto pairs (BTC, ETH, SOL) from Binance
- Fetches the current USD → KES exchange rate from Frankfurter
- Converts each crypto price into KES
- Persists results to a PostgreSQL database
- Prints a clean, formatted report to the terminal
- Fully containerized with Docker Compose (app + database)

## Tech Stack

- Python 3.14
- `requests` — API calls
- `SQLAlchemy` + `psycopg2` — PostgreSQL access
- `python-dotenv` — environment variable management
- PostgreSQL 16
- Docker & Docker Compose
- `uv` — dependency management (local development)

## Prerequisites

- Docker and Docker Compose installed
- (Optional, for local development outside Docker) [`uv`](https://docs.astral.sh/uv/) installed

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/Daboz-cell/crypto_rate_etl.git
   cd crypto_rate_etl
```

2. Create a `.env` file in the project root with the following variables:
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_HOST=localhost
DB_PORT=5433


3. Build and run with Docker Compose:
```bash
   docker compose up --build
```

   This starts a PostgreSQL container and the ETL app container. The app fetches, converts, stores, and prints the report, then exits.

## Usage

Run with one or more symbols via the `--symbol` flag (comma-separated for multiple):

```bash
docker compose run --rm app --symbol BTCUSDT
docker compose run --rm app --symbol BTCUSDT,ETHUSDT,SOLUSDT
```

Running without `--symbol` prints usage instructions instead of crashing:

```bash
docker compose run --rm app
usage: main.py [-h] --symbol SYMBOL
main.py: error: the following arguments are required: --symbol
```

## Error Handling

The application catches common failure cases and exits cleanly instead of dumping a raw Python traceback:

- **No internet / API unreachable** — prints a network error message and exits with status code 1
- **API request times out** — prints a timeout message and exits with status code 1
- **Database unreachable** (wrong credentials, container not running) — prints a database error message and exits with status code 1

Example:
```bash
uv run python main.py --symbol BTCUSDT
Network ERROR: Unable to connect to the API. Please check your internet connection.
```

Every failure path exits with a non-zero status code, so the application can be used safely inside a scheduler or CI pipeline.

## Project Structure

crypto_rate_ETL/
├── app/
│ ├── extractor.py # Fetches raw data from Binance + Frankfurter APIs
│ ├── transformer.py # Converts USD prices to KES
│ ├── loader.py # Writes results to PostgreSQL
│ └── init.py
├── main.py # Entry point — runs the full ETL pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env # Not committed — holds DB credentials
└── README.md