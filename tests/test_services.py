import pytest

from src.services import cashback_categories, find_phone_transactions, investment_bank


@pytest.fixture
def sample_transactions():
    return [
        {"Дата операции": "2023-01-01", "Категория": "Еда", "Кешбэк": 10},
        {"Дата операции": "2023-01-15", "Категория": "Еда", "Кешбэк": 20},
        {"Дата операции": "2023-02-01", "Категория": "Транспорт", "Кешбэк": 5}
    ]

def test_cashback_categories(sample_transactions):
    """Проверяем расчет кешбэка по категориям."""
    result = cashback_categories(sample_transactions, 2023, 1)
    assert result == {"Еда": 30}

def test_investment_bank():
    """Проверяем округление для инвесткопилки."""
    transactions = [
        {"Дата операции": "2023-01-01", "Сумма операции": 123},
        {"Дата операции": "2023-01-02", "Сумма операции": 177}
    ]
    assert investment_bank("2023-01", transactions, 50) == 50  # (150-123) + (200-177)

def test_find_phone_transactions():
    """Проверяем поиск транзакций с номерами телефонов."""
    transactions = [
        {"Описание": "Пополнение +7 921 123-45-67"},
        {"Описание": "Оплата интернета"}
    ]
    result = find_phone_transactions(transactions)
    assert len(result) == 1
    assert "+7 921 123-45-67" in result[0]["Описание"]