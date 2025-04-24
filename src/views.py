"""Views for generating JSON responses for web pages."""
import json
from datetime import datetime
from typing import Dict, Any

import pandas as pd

from .utils import get_greeting, get_currency_rates, get_stock_prices


def main_page(date_time: str, df: pd.DataFrame) -> Dict[str, Any]:
    """Generate JSON response for main page."""
    try:
        current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        # Get cards summary
        cards_summary = []
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
        with open('user_settings.json', 'r') as f:
            settings = json.load(f)

        response = {
            "greeting": get_greeting(current_time),
            "cards": cards_summary,
            "top_transactions": top_transactions,
            "currency_rates": get_currency_rates(settings['user_currencies']),
            "stock_prices": get_stock_prices(settings['user_stocks'])
        }

        return response
    except Exception as e:
        raise ValueError(f"Error generating main page response: {e}")