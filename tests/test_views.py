import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.views import main_page, events_page

@pytest.fixture
def mock_transactions():
    return [
        {"Дата операции": "2023-01-01", "Сумма платежа": 1000, "Категория": "Еда", "Описание": "Покупка еды"},
        {"Дата операции": "2023-01-02", "Сумма платежа": -500, "Категория": "Транспорт", "Описание": "Такси"}
    ]

def test_main_page_greeting():
    """Проверяем, что приветствие зависит от времени."""
    assert main_page("2023-01-01 08:00:00")["greeting"] == "Доброе утро"
    assert main_page("2023-01-01 15:00:00")["greeting"] == "Добрый день"

@patch("src.views.load_transactions")
def test_main_page_returns_correct_structure(mock_load):
    """Проверяем структуру ответа главной страницы."""
    mock_load.return_value = MagicMock()
    result = main_page("2023-01-01 12:00:00")
    assert "greeting" in result
    assert "top_transactions" in result

@patch("src.views.filter_transactions_by_date")
def test_events_page_with_month_period(mock_filter):
    """Проверяем фильтрацию по месяцу."""
    mock_filter.return_value = MagicMock()
    result = events_page("2023-01-15", "M")
    assert "expenses" in result
    assert "income" in result