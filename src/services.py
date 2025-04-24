"""Services for analyzing financial data."""
import json
import logging
from typing import Dict, List, Any

import pandas as pd

logger = logging.getLogger(__name__)


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Search transactions by query in description or category."""
    try:
        matching_transactions = []

        for transaction in transactions:
            description = str(transaction.get('Описание', '')).lower()
            category = str(transaction.get('Категория', '')).lower()
            query = query.lower()

            if query in description or query in category:
                matching_transactions.append(transaction)

        return {
            "matching_transactions": matching_transactions,
            "total_found": len(matching_transactions)
        }
    except Exception as e:
        logger.error(f"Error in simple search: {e}")
        raise