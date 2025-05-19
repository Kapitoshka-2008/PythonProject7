import logging
from typing import Any, Dict, List

import pandas as pd


def cashback_categories(
    transactions: List[Dict[str, Any]], 
    year: int, 
    month: int
) -> Dict[str, float]:
    """Возвращает сумму кешбэка по категориям за месяц."""
    try:
        result = {}
        for tx in transactions:
            tx_date = pd.to_datetime(tx["Дата операции"])
            if tx_date.year == year and tx_date.month == month:
                category = tx["Категория"]
                result[category] = result.get(category, 0) + tx.get("Кешбэк", 0)
        return result
    except Exception as e:
        logging.error(f"Ошибка в cashback_categories: {e}")
        return {}

import math


def investment_bank(
    month: str,
    transactions: List[Dict[str, Any]],
    limit: int = 10
) -> float:
    """Считает сумму для инвесткопилки."""
    total = 0.0
    for tx in transactions:
        if tx["Дата операции"].startswith(month):
            rounded = math.ceil(tx["Сумма операции"] / limit) * limit
            total += rounded - tx["Сумма операции"]
    return round(total, 2)

import re


def find_phone_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ищет транзакции с номерами телефонов в описании."""
    phone_pattern = re.compile(r"\+7\s?\d{3}\s?\d{3}[- ]?\d{2}[- ]?\d{2}")
    result = []
    for tx in transactions:
        if "Описание" in tx and phone_pattern.search(tx["Описание"]):
            result.append(tx)
    return result