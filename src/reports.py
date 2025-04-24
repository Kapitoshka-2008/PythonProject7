"""Reports generation module."""
import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd


def save_report(filename: Optional[str] = None):
    """Decorator to save report results to file."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            # Generate filename if not provided
            actual_filename = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Save results to file
            with open(actual_filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> dict:
    """Generate report of spending by category for last 3 months."""
    try:
        # Use current date if not provided
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d")

        # Calculate start date (3 months ago)
        start_date = end_date - timedelta(days=90)

        # Convert date column to datetime if it's not
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

        # Filter transactions
        mask = (
                (transactions['Дата операции'] >= start_date) &
                (transactions['Дата операции'] <= end_date) &
                (transactions['Категория'] == category)
        )

        filtered_df = transactions[mask]

        # Calculate statistics
        total_spent = abs(filtered_df[filtered_df['Сумма операции'] < 0]['Сумма операции'].sum())
        transaction_count = len(filtered_df)
        avg_transaction = total_spent / transaction_count if transaction_count > 0 else 0

        return {
            "category": category,
            "period": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            "statistics": {
                "total_spent": round(total_spent, 2),
                "transaction_count": transaction_count,
                "average_transaction": round(avg_transaction, 2)
            },
            "transactions": filtered_df[['Дата операции', 'Сумма операции', 'Описание']]
            .to_dict('records')
        }
    except Exception as e:
        raise ValueError(f"Error generating category spending report: {e}")