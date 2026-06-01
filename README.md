# Binance Futures Testnet Trading Bot

A clean Python CLI for placing orders on Binance Futures Testnet (USDT-M).  
Supports **MARKET**, **LIMIT**, and **STOP_MARKET** orders with structured logging and full input validation.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # python-binance wrapper
│   ├── orders.py          # MARKET / LIMIT / STOP_MARKET logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Dual handler: file (DEBUG) + console (INFO)
├── logs/
│   └── trading.log        # Generated on first run
├── cli.py                 # CLI entry point
├── .env.example           # Rename to .env and add your keys
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone <repo-url>
cd Trading_Bot_Binance_Testnet
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Binance Futures Testnet API keys
1. Go to https://testnet.binancefuture.com
2. Log in → **API Management** → Generate API Key (System generated)
3. Copy the **API Key** and **Secret Key**

### 5. Configure credentials
```bash

cp .env.example .env
# Edit .env and paste your keys

```

---

## Usage

### Place a MARKET order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# OR

python3 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 72000

# OR

python3 cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 72000
```

### Place a STOP_MARKET order (bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 65000

# OR

python3 cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 65000

```

### Help
```bash
python cli.py --help

# OR

python3 cli.py --help
```

---

## Sample Output

```
  ┌─────────────────────────────────────┐
  │          ORDER REQUEST               │
  └─────────────────────────────────────┘
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001

  ┌─────────────────────────────────────┐
  │          ORDER RESPONSE              │
  └─────────────────────────────────────┘
  Order ID      : 4156231897
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Status        : FILLED
  Orig Qty      : 0.001
  Executed Qty  : 0.001
  Avg Price     : 67430.50000
  Limit Price   : 0
  Time-in-Force : GTC

  ✔  Order placed successfully!
```

---

## Logging

All activity is written to `logs/trading.log`:
- **DEBUG**: full API request parameters and raw responses
- **INFO**: order summaries and outcomes
- **ERROR**: API errors, validation failures, network issues

Console shows INFO+ only; the log file captures everything.

---

## Assumptions

- Targets Binance Futures Testnet (USDT-M) via `python-binance testnet=True`
- Credentials are stored in `.env` (never committed to git)
- Quantity/price precision must match the symbol's exchange filters; if Binance returns error `-1111`, adjust your values to the correct decimal places (e.g. BTC quantity in steps of 0.001)
- `timeInForce` defaults to `GTC` for LIMIT orders; override with `--tif IOC` if needed
- STOP_MARKET is the bonus third order type
