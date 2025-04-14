import pandas as pd
from datetime import datetime, timedelta
from typing import Dict

def spending_by_category(
        df: pd.DataFrame,
        category: str,
        date: str = None
) -> Dict[str, float]:
    """Считает траты по категории за 3 месяца."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    end_date = pd.to_datetime(date)
    start_date = end_date - timedelta(days=90)

    filtered = df[
        (df["Категория"] == category) &
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ]
    return {"total": filtered["Сумма платежа"].sum()}

def spending_by_weekday(df: pd.DataFrame, date: str = None) -> Dict[str, float]:
    """Средние траты по дням недели."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    end_date = pd.to_datetime(date)
    start_date = end_date - timedelta(days=90)

    filtered = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ]
    filtered["День недели"] = filtered["Дата операции"].dt.day_name()
    return filtered.groupby("День недели")["Сумма платежа"].mean().to_dict()