from utils import load_transactions, filter_transactions_by_date
from typing import Dict
import json
import logging


def get_greeting(time_str: str) -> str:
    """Возвращает приветствие по времени."""
    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").time()
    if 5 <= time.hour < 12:
        return "Доброе утро"
    elif 12 <= time.hour < 18:
        return "Добрый день"
    elif 18 <= time.hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def main_page(date_time: str, file_path: str = "data/operations.xlsx") -> Dict:
    """Генерирует JSON для главной страницы."""
    try:
        df = load_transactions(file_path)
        greeting = get_greeting(date_time)

        # Топ-5 транзакций
        top_transactions = (
            df.sort_values("Сумма платежа", ascending=False)
            .head(5)[["Дата операции", "Сумма платежа", "Категория", "Описание"]]
            .to_dict(orient="records")
        )

        # Курсы валют (заглушка)
        currency_rates = [
            {"currency": "USD", "rate": 73.21},
            {"currency": "EUR", "rate": 87.08}
        ]

        return {
            "greeting": greeting,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
        }
    except Exception as e:
        logging.error(f"Ошибка в main_page: {e}")
        return {"error": str(e)}


def events_page(date_time: str, period: str = "M", file_path: str = "data/operations.xlsx") -> Dict:
    """Анализ трат и поступлений за период."""
    try:
        df = load_transactions(file_path)
        filtered_df = filter_transactions_by_date(df, date_time, period)

        # Расходы
        expenses = filtered_df[filtered_df["Сумма платежа"] < 0]
        expenses_main = (
            expenses.groupby("Категория")["Сумма платежа"]
            .sum()
            .sort_values(ascending=False)
            .head(7)
            .to_dict()
        )

        # Поступления
        income = filtered_df[filtered_df["Сумма платежа"] > 0]
        income_main = (
            income.groupby("Категория")["Сумма платежа"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )

        return {
            "expenses": {
                "total_amount": round(expenses["Сумма платежа"].sum()),
                "main": [{"category": k, "amount": abs(v)} for k, v in expenses_main.items()],
            },
            "income": {
                "total_amount": round(income["Сумма платежа"].sum()),
                "main": [{"category": k, "amount": v} for k, v in income_main.items()],
            },
        }
    except Exception as e:
        logging.error(f"Ошибка в events_page: {e}")
        return {"error": str(e)}