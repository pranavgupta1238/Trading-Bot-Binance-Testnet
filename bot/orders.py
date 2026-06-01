"""Order placement logic — one function per order type."""

from binance.client import Client
from binance.exceptions import BinanceAPIException

from bot.logging_config import setup_logger

logger = setup_logger()


def _format_response(r: dict) -> str:
    return (
        f"\n"
        f"  ┌─────────────────────────────────────┐\n"
        f"  │          ORDER RESPONSE              │\n"
        f"  └─────────────────────────────────────┘\n"
        f"  Order ID      : {r.get('orderId')}\n"
        f"  Symbol        : {r.get('symbol')}\n"
        f"  Side          : {r.get('side')}\n"
        f"  Type          : {r.get('type')}\n"
        f"  Status        : {r.get('status')}\n"
        f"  Orig Qty      : {r.get('origQty')}\n"
        f"  Executed Qty  : {r.get('executedQty')}\n"
        f"  Avg Price     : {r.get('avgPrice', 'N/A')}\n"
        f"  Limit Price   : {r.get('price', 'N/A')}\n"
        f"  Time-in-Force : {r.get('timeInForce', 'N/A')}\n"
    )


def place_market_order(client: Client, symbol: str, side: str, quantity: float) -> dict:
    logger.info("Placing MARKET order | %s %s qty=%s", symbol, side, quantity)
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        logger.info(
            "MARKET order SUCCESS | orderId=%s status=%s executedQty=%s avgPrice=%s",
            response.get("orderId"),
            response.get("status"),
            response.get("executedQty"),
            response.get("avgPrice"),
        )
        logger.debug("Full response: %s", response)
        return response
    except BinanceAPIException as e:
        logger.error("MARKET order FAILED | code=%s msg=%s", e.code, e.message)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise


def place_limit_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    logger.info(
        "Placing LIMIT order | %s %s qty=%s price=%s tif=%s",
        symbol, side, quantity, price, time_in_force,
    )
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce=time_in_force,
        )
        logger.info(
            "LIMIT order SUCCESS | orderId=%s status=%s price=%s",
            response.get("orderId"),
            response.get("status"),
            response.get("price"),
        )
        logger.debug("Full response: %s", response)
        return response
    except BinanceAPIException as e:
        logger.error("LIMIT order FAILED | code=%s msg=%s", e.code, e.message)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise


def place_stop_market_order(
    client: Client,
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
) -> dict:
    """Bonus: STOP_MARKET — triggers a market order when stopPrice is hit."""
    logger.info(
        "Placing STOP_MARKET order | %s %s qty=%s stopPrice=%s",
        symbol, side, quantity, stop_price,
    )
    try:
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            quantity=quantity,
            stopPrice=stop_price,
        )
        logger.info(
            "STOP_MARKET order SUCCESS | orderId=%s status=%s",
            response.get("orderId"),
            response.get("status"),
        )
        logger.debug("Full response: %s", response)
        return response
    except BinanceAPIException as e:
        logger.error("STOP_MARKET order FAILED | code=%s msg=%s", e.code, e.message)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise


def format_response(r: dict) -> str:
    return _format_response(r)
