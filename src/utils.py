"""Utility functions for the finance analyzer."""
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_transactions(file_path: str) -> pd.DataFrame:
    """Load transactions from Excel file."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Successfully loaded transactions from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading transactions: {e}")
        raise

def get_greeting(time: datetime) -> str:
    """Return appropriate greeting based on time of day."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Get current currency rates."""
    # Implement actual API call here
    return [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]

def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Get current stock prices."""
    # Implement actual API call here
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08}
    ]