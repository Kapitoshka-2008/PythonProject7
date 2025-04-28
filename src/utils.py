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
        # Пробуем определить формат файла по расширению
        if file_path.endswith('.xlsx'):
            engine = 'openpyxl'
        elif file_path.endswith('.xls'):
            engine = 'xlrd'
        else:
            # Если расширение не определено, пробуем openpyxl
            engine = 'openpyxl'
            
        df = pd.read_excel(file_path, engine=engine)
        
        # Проверяем наличие необходимых колонок
        required_columns = ["Дата операции", "Сумма операции", "Категория", "Описание"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.warning(f"Отсутствуют колонки: {missing_columns}")
            # Добавляем отсутствующие колонки с пустыми значениями
            for col in missing_columns:
                df[col] = None
                
        # Преобразуем даты
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%Y-%m-%d", errors='coerce')
            
        logger.info(f"Successfully loaded transactions from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading transactions: {e}")
        # Возвращаем пустой DataFrame с необходимыми колонками
        return pd.DataFrame(columns=["Дата операции", "Сумма операции", "Категория", "Описание", "Номер карты"])

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

def save_transactions(df: pd.DataFrame, file_path: str) -> None:
    """Save transactions to Excel file."""
    try:
        df.to_excel(file_path, index=False)
        logger.info(f"Successfully saved transactions to {file_path}")
    except Exception as e:
        logger.error(f"Error saving transactions: {e}")
        raise