"""Report generation functions for the finance analyzer."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def handle_empty_dataframe(func):
    """Decorator to handle empty DataFrame cases."""
    def wrapper(df: pd.DataFrame, *args, **kwargs):
        if df.empty:
            logger.warning(f"Empty DataFrame passed to {func.__name__}")
            return None
        return func(df, *args, **kwargs)
    return wrapper


@handle_empty_dataframe
def spending_by_category(
    df: pd.DataFrame,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, float]:
    """Calculate total spending by category for a given date range."""
    try:
        # Filter by date range if provided
        if start_date and end_date:
            mask = (
                (df["Дата операции"] >= start_date) &
                (df["Дата операции"] <= end_date)
            )
            df = df[mask]

        # Group by category and sum amounts
        spending = df.groupby("Категория")["Сумма операции"].sum().to_dict()
        return spending
    except Exception as e:
        logger.error(f"Error in spending_by_category: {e}")
        return {}


@handle_empty_dataframe
def spending_by_weekday(
    df: pd.DataFrame,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, float]:
    """Calculate average spending by weekday for a given date range."""
    try:
        # Filter by date range if provided
        if start_date and end_date:
            mask = (
                (df["Дата операции"] >= start_date) &
                (df["Дата операции"] <= end_date)
            )
            df = df[mask]

        # Add weekday column
        df["weekday"] = df["Дата операции"].dt.day_name()

        # Group by weekday and calculate mean
        spending = df.groupby("weekday")["Сумма операции"].mean().to_dict()
        return spending
    except Exception as e:
        logger.error(f"Error in spending_by_weekday: {e}")
        return {}


@handle_empty_dataframe
def top_transactions(
    df: pd.DataFrame,
    n: int = 5,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict]:
    """Get top N transactions by amount for a given date range."""
    try:
        # Filter by date range if provided
        if start_date and end_date:
            mask = (
                (df["Дата операции"] >= start_date) &
                (df["Дата операции"] <= end_date)
            )
            df = df[mask]

        # Sort by amount and get top N
        top_n = df.nlargest(n, "Сумма операции")
        return top_n.to_dict("records")
    except Exception as e:
        logger.error(f"Error in top_transactions: {e}")
        return []
