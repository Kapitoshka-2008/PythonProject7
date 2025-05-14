"""Utility functions for the finance analyzer."""
import json
import logging
from datetime import datetime
from typing import Any, Dict, List
import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Получаем API ключи из переменных окружения
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
STOCK_API_KEY = os.getenv("STOCK_API_KEY")

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
    """Get current currency rates from ExchangeRate-API."""
    if not CURRENCY_API_KEY:
        logger.error("CURRENCY_API_KEY not found in .env file.")
        return [{"currency": cur, "rate": "Error: API key missing"} for cur in currencies]

    result = []
    # Базовая валюта для ExchangeRate-API (например, USD, или можно сделать RUB, если API поддерживает)
    # Для бесплатного тарифа ExchangeRate-API часто базовая валюта USD
    base_currency = "USD" 
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{base_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        data = response.json()

        if data.get("result") == "error":
            error_type = data.get("error-type", "Unknown error")
            logger.error(f"ExchangeRate-API error: {error_type}")
            # Возвращаем ошибку для каждой запрашиваемой валюты
            return [{"currency": cur, "rate": f"API Error: {error_type}"} for cur in currencies]

        rates = data.get("conversion_rates")
        if not rates:
            logger.error("No conversion_rates found in ExchangeRate-API response.")
            return [{"currency": cur, "rate": "API Error: No rates data"} for cur in currencies]

        for currency_code in currencies:
            if currency_code == base_currency: # Если запрашиваем базовую валюту
                result.append({"currency": currency_code, "rate": 1.0})
                continue
            if currency_code == "RUB" and base_currency != "RUB": # Пример конвертации в RUB, если база USD
                 # Нужно найти курс RUB к USD и инвертировать его, если API не дает прямой курс к RUB от USD
                 # Либо, если API позволяет, указать RUB как базовую или целевую.
                 # В данном случае, мы ожидаем, что RUB есть в rates по отношению к base_currency.
                pass # Оставляем как есть, если RUB есть в rates

            rate = rates.get(currency_code)
            if rate is not None:
                result.append({"currency": currency_code, "rate": round(float(rate), 4)})
            else:
                logger.warning(f"Currency {currency_code} not found in ExchangeRate-API response for base {base_currency}.")
                result.append({"currency": currency_code, "rate": "Not found"})
        
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting currency rates from ExchangeRate-API: {e}")
        return [{"currency": cur, "rate": "Network Error"} for cur in currencies]
    except Exception as e:
        logger.error(f"Unexpected error in get_currency_rates: {e}")
        return [{"currency": cur, "rate": "Unexpected Error"} for cur in currencies]

def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Get current stock prices from Alpha Vantage API."""
    if not STOCK_API_KEY:
        logger.error("STOCK_API_KEY not found in .env file.")
        return [{"stock": stock, "price": "Error: API key missing"} for stock in stocks]

    result = []
    for stock_symbol in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={STOCK_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Проверяем ответ от Alpha Vantage
            if "Global Quote" in data and data["Global Quote"] and "05. price" in data["Global Quote"]:
                price = data["Global Quote"]["05. price"]
                result.append({"stock": stock_symbol, "price": round(float(price), 2)})
            elif "Error Message" in data:
                logger.warning(f"Alpha Vantage API error for {stock_symbol}: {data['Error Message']}")
                result.append({"stock": stock_symbol, "price": "API Error"})
            elif "Note" in data: # Alpha Vantage часто возвращает "Note" при превышении лимита запросов
                logger.warning(f"Alpha Vantage API Note for {stock_symbol}: {data['Note']}")
                result.append({"stock": stock_symbol, "price": "API Limit/Error"})
            else:
                logger.warning(f"Unexpected response structure from Alpha Vantage for {stock_symbol}: {data}")
                result.append({"stock": stock_symbol, "price": "Invalid data"})
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting stock price for {stock_symbol} from Alpha Vantage: {e}")
            result.append({"stock": stock_symbol, "price": "Network Error"})
        except Exception as e: # Ловим другие возможные ошибки (например, float conversion)
            logger.error(f"Unexpected error processing stock {stock_symbol}: {e}")
            result.append({"stock": stock_symbol, "price": "Processing Error"})
            
    return result

def save_transactions(df: pd.DataFrame, file_path: str) -> None:
    """Save transactions to Excel file."""
    try:
        df.to_excel(file_path, index=False)
        logger.info(f"Successfully saved transactions to {file_path}")
    except Exception as e:
        logger.error(f"Error saving transactions: {e}")
        raise