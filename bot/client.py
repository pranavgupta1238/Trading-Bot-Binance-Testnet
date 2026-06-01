"""Thin wrapper around python-binance for Futures Testnet."""

import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()


def get_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        raise EnvironmentError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file."
        )

    logger.debug("Creating Binance Futures Testnet client …")
    client = Client(api_key, api_secret, testnet=True)
    return client
