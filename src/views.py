"""Views for generating web pages."""

import json
import logging
from datetime import datetime
from typing import Any, Dict

import pandas as pd
from flask import render_template

from .utils import get_currency_rates, get_greeting, get_stock_prices, load_transactions


def filter_transactions_by_date(df: pd.DataFrame, date_str: str, period: str = "M") -> pd.DataFrame:
    """Filter transactions by date period."""
    try:
        date = pd.to_datetime(date_str)
        if period == "D":
            start_date = date - pd.DateOffset(days=1)
        elif period == "M":
            start_date = date - pd.DateOffset(months=1)
        elif period == "Q":
            start_date = date - pd.DateOffset(months=3)
        elif period == "Y":
            start_date = date - pd.DateOffset(years=1)
        else:
            raise ValueError(f"Unknown period: {period}")
        return df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= date)]
    except Exception as e:
        logging.error(f"Error filtering transactions: {e}")
        return pd.DataFrame()


def main_page(date_time: str, df: pd.DataFrame = None) -> Dict[str, Any]:
    """Generate main page."""
    try:
        current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        if df is None:
            try:
                df = load_transactions("data/operations.xlsx")
            except Exception as e:
                logging.error(f"Error loading transactions: {e}")
                return render_template(
                    "pages/main.html",
                    greeting=get_greeting(current_time),
                    top_transactions={"expenses": [], "income": []},
                )

        # Get top transactions
        top_transactions = {"expenses": [], "income": []}
        if all(col in df.columns for col in ["Сумма операции", "Дата операции", "Категория", "Описание"]):
            # Фильтруем строки с корректными датами
            valid_dates_df = df[df["Дата операции"].notna()]
            if not valid_dates_df.empty:
                # Расходы
                expenses = valid_dates_df[valid_dates_df["Сумма операции"] < 0].sort_values("Сумма операции").head(5)
                top_transactions["expenses"] = expenses.apply(
                    lambda x: {
                        "date": x["Дата операции"].strftime("%Y-%m-%d"),
                        "amount": round(float(x["Сумма операции"]), 2),
                        "description": str(x["Описание"]) if pd.notna(x["Описание"]) else "Unknown",
                    },
                    axis=1,
                ).tolist()

                # Доходы
                income = valid_dates_df[valid_dates_df["Сумма операции"] > 0].sort_values("Сумма операции", ascending=False).head(5)
                top_transactions["income"] = income.apply(
                    lambda x: {
                        "date": x["Дата операции"].strftime("%Y-%m-%d"),
                        "amount": round(float(x["Сумма операции"]), 2),
                        "description": str(x["Описание"]) if pd.notna(x["Описание"]) else "Unknown",
                    },
                    axis=1,
                ).tolist()

        return render_template(
            "pages/main.html",
            greeting=get_greeting(current_time),
            top_transactions=top_transactions,
        )
    except Exception as e:
        logging.error(f"Error generating main page: {e}")
        return render_template(
            "pages/main.html",
            greeting=get_greeting(current_time),
            error=str(e),
        )


def events_page(date_time: str, period: str = "M", file_path: str = "data/operations.xlsx") -> Dict:
    """Анализ трат и поступлений за период."""
    try:
        df = load_transactions(file_path)
        filtered_df = filter_transactions_by_date(df, date_time, period)

        # Расходы
        expenses = filtered_df[filtered_df["Сумма операции"] < 0]
        expenses_list = expenses.apply(
            lambda x: {
                "date": x["Дата операции"].strftime("%Y-%m-%d"),
                "amount": round(float(x["Сумма операции"]), 2),
                "description": str(x["Описание"]) if pd.notna(x["Описание"]) else "Unknown",
            },
            axis=1,
        ).tolist()

        # Поступления
        income = filtered_df[filtered_df["Сумма операции"] > 0]
        income_list = income.apply(
            lambda x: {
                "date": x["Дата операции"].strftime("%Y-%m-%d"),
                "amount": round(float(x["Сумма операции"]), 2),
                "description": str(x["Описание"]) if pd.notna(x["Описание"]) else "Unknown",
            },
            axis=1,
        ).tolist()

        return render_template(
            "pages/events.html",
            period=period,
            expenses=expenses_list,
            income=income_list,
        )
    except Exception as e:
        logging.error(f"Ошибка в events_page: {e}")
        return render_template(
            "pages/events.html",
            period=period,
            expenses=[],
            income=[],
            error=str(e),
        )
