import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel и преобразует дату."""
    try:
        df = pd.read_excel(file_path)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])
        return df
    except Exception as e:
        logging.error(f"Ошибка загрузки данных: {e}")
        raise


def filter_transactions_by_date(
        df: pd.DataFrame,
        date: str,
        period: str = "M"
) -> pd.DataFrame:
    """Фильтрует транзакции по периоду (месяц, год и т.д.)."""
    date = pd.to_datetime(date)
    if period == "W":  # Неделя
        start_date = date - pd.Timedelta(days=date.weekday())
        end_date = start_date + pd.Timedelta(days=6)
    elif period == "M":  # Месяц
        start_date = date.replace(day=1)
        end_date = (start_date + pd.offsets.MonthEnd(0))
    elif period == "Y":  # Год
        start_date = date.replace(month=1, day=1)
        end_date = date.replace(month=12, day=31)
    else:  # ALL – все данные до даты
        start_date = pd.Timestamp.min
        end_date = date

    return df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]