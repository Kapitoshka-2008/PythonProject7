"""Views for generating JSON responses for web pages."""
import json
import logging
from datetime import datetime
from typing import Dict, Any

import pandas as pd

from .utils import get_greeting, get_currency_rates, get_stock_prices, load_transactions


def filter_transactions_by_date(df: pd.DataFrame, date_str: str, period: str = "M") -> pd.DataFrame:
    """Filter transactions by date period."""
    try:
        date = pd.to_datetime(date_str)
        if period == "M":
            start_date = date - pd.DateOffset(months=1)
        elif period == "Q":
            start_date = date - pd.DateOffset(months=3)
        elif period == "Y":
            start_date = date - pd.DateOffset(years=1)
        else:
            raise ValueError(f"Unknown period: {period}")
        
        return df[
            (df["Дата операции"] >= start_date) &
            (df["Дата операции"] <= date)
        ]
    except Exception as e:
        logging.error(f"Error filtering transactions: {e}")
        raise


def main_page(date_time: str, df: pd.DataFrame = None) -> Dict[str, Any]:
    """Generate JSON response for main page."""
    try:
        current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        
        if df is None:
            try:
                df = load_transactions("data/operations.xlsx")
            except Exception as e:
                logging.error(f"Error loading transactions: {e}")
                # Возвращаем базовый ответ без данных о транзакциях
                return {
                    "greeting": get_greeting(current_time),
                    "cards": [],
                    "top_transactions": [],
                    "currency_rates": get_currency_rates(['USD', 'EUR']),
                    "stock_prices": get_stock_prices(['AAPL', 'GOOGL'])
                }

        # Get cards summary
        cards_summary = []
        if 'Номер карты' in df.columns:
            for card in df['Номер карты'].unique():
                if pd.isna(card):
                    continue
                card_df = df[df['Номер карты'] == card]
                total_spent = abs(card_df[card_df['Сумма операции'] < 0]['Сумма операции'].sum())
                cashback = total_spent * 0.01  # 1% cashback
                cards_summary.append({
                    "last_digits": str(card),
                    "total_spent": round(total_spent, 2),
                    "cashback": round(cashback, 2)
                })

        # Get top 5 transactions
        top_transactions = []
        if all(col in df.columns for col in ['Сумма операции', 'Дата операции', 'Категория', 'Описание']):
            top_transactions = (
                df.sort_values('Сумма операции', ascending=False)
                .head(5)
                .apply(
                    lambda x: {
                        "date": x['Дата операции'].strftime("%d.%m.%Y"),
                        "amount": round(x['Сумма операции'], 2),
                        "category": x['Категория'],
                        "description": x['Описание']
                    },
                    axis=1
                ).tolist()
            )

        # Load user settings
        try:
            with open('user_settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {
                'user_currencies': ['USD', 'EUR'],
                'user_stocks': ['AAPL', 'GOOGL']
            }

        response = {
            "greeting": get_greeting(current_time),
            "cards": cards_summary,
            "top_transactions": top_transactions,
            "currency_rates": get_currency_rates(settings['user_currencies']),
            "stock_prices": get_stock_prices(settings['user_stocks'])
        }

        return response
    except Exception as e:
        logging.error(f"Error generating main page response: {e}")
        return {
            "greeting": get_greeting(current_time),
            "error": str(e)
        }


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
        return {
            "expenses": {"total_amount": 0, "main": []},
            "income": {"total_amount": 0, "main": []},
            "error": str(e)
        }