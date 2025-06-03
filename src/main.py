"""Main module for running the finance analyzer."""

import logging

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import load_transactions


def main():
    """Main function to run the finance analyzer."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Load transactions
        df = load_transactions("data/operations.xlsx")

        # Generate main page response
        logger.info("Generated main page response")

        # Example of simple search
        transactions = df.to_dict("records")
        search_results = simple_search("супермаркет", transactions)
        logger.info(f"Found {search_results['total_found']} matching transactions")

        # Generate category spending report
        report = spending_by_category(df, "Супермаркеты")
        logger.info(f"Generated spending report for category 'Супермаркеты'")


    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    main()
