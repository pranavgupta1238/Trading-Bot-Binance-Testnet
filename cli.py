#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI

Usage:
  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.001 --price 72000
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 65000
"""

import argparse
import sys

from binance.exceptions import BinanceAPIException

from bot.client import get_client
from bot.logging_config import setup_logger
from bot.orders import place_market_order, place_limit_order, place_stop_market_order, format_response
from bot.validators import (
    ValidationError,
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)

logger = setup_logger()


def print_request_summary(symbol, side, order_type, quantity, price=None, stop_price=None):
    print()
    print("  ┌─────────────────────────────────────┐")
    print("  │          ORDER REQUEST               │")
    print("  └─────────────────────────────────────┘")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        print(f"  Price      : {price}")
    if stop_price is not None:
        print(f"  Stop Price : {stop_price}")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet — place MARKET, LIMIT, or STOP_MARKET orders",
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.001 --price 72000
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 65000
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--symbol",     required=True,            help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,            help="BUY or SELL")
    parser.add_argument("--type",       required=True, dest="order_type",
                        help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity",   required=True, type=float, help="Order quantity")
    parser.add_argument("--price",      type=float, default=None, help="Limit price (LIMIT orders)")
    parser.add_argument("--stop-price", type=float, default=None, dest="stop_price",
                        help="Stop trigger price (STOP_MARKET orders)")
    parser.add_argument("--tif",        default="GTC",
                        help="Time-in-force for LIMIT orders (default: GTC)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # --- validate ---
    try:
        symbol     = validate_symbol(args.symbol)
        side       = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity   = validate_quantity(args.quantity)
        price      = validate_price(args.price, order_type)
        stop_price = validate_stop_price(args.stop_price, order_type)
    except ValidationError as e:
        logger.error("Validation failed: %s", e)
        print(f"\n  ✘  {e}\n")
        sys.exit(1)

    print_request_summary(symbol, side, order_type, quantity, price, stop_price)

    # --- place order ---
    try:
        client = get_client()

        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(client, symbol, side, quantity, price, args.tif.upper())
        elif order_type == "STOP_MARKET":
            response = place_stop_market_order(client, symbol, side, quantity, stop_price)

        print(format_response(response))
        print("  ✔  Order placed successfully!\n")

    except BinanceAPIException as e:
        print(f"\n  ✘  Binance API Error [{e.code}]: {e.message}\n")
        sys.exit(1)
    except EnvironmentError as e:
        print(f"\n  ✘  Config error: {e}\n")
        sys.exit(1)
    except (ConnectionError, TimeoutError) as e:
        print(f"\n  ✘  Network error: {e}\n")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"\n  ✘  Unexpected error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
