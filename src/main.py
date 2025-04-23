import pandas as pd
from src.views import main_page, events_page
from src.services import cashback_categories, investment_bank
from src.reports import spending_by_category
from src.utils import load_transactions
from pathlib import Path

def run_analysis():
    # Проверяем, есть ли файл данных
    data_path = "data/operations.xlsx"
    if not Path(data_path).exists():
        print("Файл данных не найден. Создаю тестовый...")
        from data.generate_data import generate_test_excel
        generate_test_excel(data_path)

    # Загружаем данные
    df = load_transactions(data_path)
    transactions = df.to_dict("records")

    # Примеры вызовов функций
    print("\n=== Главная страница ===")
    print(main_page("2023-01-01 12:00:00", data_path))

    print("\n=== События (месяц) ===")
    print(events_page("2023-01-15", "M", data_path))

    print("\n=== Кешбэк по категориям (январь 2023) ===")
    print(cashback_categories(transactions, 2023, 1))

    print("\n=== Инвесткопилка (лимит 50 руб) ===")
    print(investment_bank("2023-01", transactions, 50))

    print("\n=== Траты по категории 'Еда' ===")
    print(spending_by_category(df, "Еда"))

if __name__ == "__main__":
    run_analysis()