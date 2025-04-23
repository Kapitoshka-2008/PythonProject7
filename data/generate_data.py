import pandas as pd
from datetime import datetime

def generate_test_excel(file_path: str = "data/operations.xlsx"):
    """Генерирует тестовый Excel-файл с транзакциями."""
    data = {
        "Дата операции": [datetime(2023, 1, 1), datetime(2023, 1, 15), datetime(2023, 2, 1)],
        "Сумма платежа": [1000, -500, 2000],
        "Категория": ["Еда", "Транспорт", "Зарплата"],
        "Описание": ["Продукты", "Такси", "Аванс"],
        "Кешбэк": [10, 0, 0],
    }
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"Сгенерирован тестовый файл: {file_path}")

if __name__ == "__main__":
    generate_test_excel()