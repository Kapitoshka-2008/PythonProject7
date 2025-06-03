from unittest.mock import MagicMock, patch
import os
import json
import pytest
import pandas as pd
import numpy as np

from src.views import events_page, main_page, filter_transactions_by_date


@pytest.fixture
def mock_transactions():
    return [
        {"Дата операции": "2023-01-01", "Сумма платежа": 1000, "Категория": "Еда", "Описание": "Покупка еды"},
        {"Дата операции": "2023-01-02", "Сумма платежа": -500, "Категория": "Транспорт", "Описание": "Такси"},
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


def test_main_page_error_loading_transactions(monkeypatch):
    """Проверяем обработку ошибки при загрузке транзакций."""
    def raise_error(*args, **kwargs):
        raise Exception("Test error")
    with patch("src.views.load_transactions", raise_error):
        result = main_page("2023-01-01 12:00:00")
        assert isinstance(result["greeting"], str)
        assert result["greeting"] in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]
        assert result["cards"] == []
        assert result["top_transactions"] == []
        assert "currency_rates" in result
        assert "stock_prices" in result


def test_main_page_missing_columns():
    """Проверяем обработку DataFrame без нужных колонок."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    result = main_page("2023-01-01 12:00:00", df)
    assert result["cards"] == []
    assert result["top_transactions"] == []


def test_main_page_empty_dataframe():
    """Проверяем обработку пустого DataFrame."""
    df = pd.DataFrame(columns=["Дата операции", "Сумма операции", "Категория", "Описание", "Номер карты"])
    result = main_page("2023-01-01 12:00:00", df)
    assert result["cards"] == []
    assert result["top_transactions"] == []


def test_main_page_no_user_settings(tmp_path, monkeypatch):
    """Проверяем поведение при отсутствии user_settings.json."""
    # Удаляем файл, если он есть
    settings_path = "user_settings.json"
    if os.path.exists(settings_path):
        os.remove(settings_path)
    df = pd.DataFrame({
        "Дата операции": [pd.Timestamp("2023-01-01")],
        "Сумма операции": [100],
        "Категория": ["Еда"],
        "Описание": ["Покупка"],
        "Номер карты": ["1234567890123456"],
    })
    result = main_page("2023-01-01 12:00:00", df)
    assert "currency_rates" in result
    assert "stock_prices" in result


def test_main_page_card_and_transaction_format():
    """Проверяем корректность формирования карточек и топ-транзакций."""
    df = pd.DataFrame({
        "Дата операции": [pd.Timestamp("2023-01-01"), pd.Timestamp("2023-01-02")],
        "Сумма операции": [-100, 200],
        "Категория": ["Еда", "Транспорт"],
        "Описание": ["Покупка", "Такси"],
        "Номер карты": ["1234567890123456", "1234567890123456"],
    })
    result = main_page("2023-01-01 12:00:00", df)
    assert result["cards"][0]["last_digits"] == "3456"
    assert isinstance(result["cards"][0]["total_spent"], (int, float, np.integer, np.floating))
    assert isinstance(result["cards"][0]["cashback"], (int, float, np.integer, np.floating))
    assert len(result["top_transactions"]) > 0
    assert "date" in result["top_transactions"][0]
    assert "amount" in result["top_transactions"][0]
    assert "category" in result["top_transactions"][0]
    assert "description" in result["top_transactions"][0]


def test_filter_transactions_by_date():
    """Проверяем функцию filter_transactions_by_date с разными периодами."""
    df = pd.DataFrame({
        "Дата операции": [pd.Timestamp("2023-01-01"), pd.Timestamp("2023-01-15"), pd.Timestamp("2023-02-01")],
        "Сумма операции": [100, 200, 300],
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Описание": ["Покупка", "Такси", "Покупка"],
        "Номер карты": ["1234567890123456", "1234567890123456", "1234567890123456"],
    })
    # Тест для периода "D" (день)
    result_d = filter_transactions_by_date(df, "2023-01-01", "D")
    assert len(result_d) == 1
    assert result_d.iloc[0]["Дата операции"] == pd.Timestamp("2023-01-01")
    # Тест для периода "M" (месяц)
    result_m = filter_transactions_by_date(df, "2023-01-15", "M")
    assert len(result_m) == 2
    # Тест для периода "Y" (год)
    result_y = filter_transactions_by_date(df, "2023-01-01", "Y")
    assert len(result_y) == 1
    # Тест для неизвестного периода
    result_unknown = filter_transactions_by_date(df, "2023-01-01", "UNKNOWN")
    assert len(result_unknown) == 0


def test_events_page_error():
    """Проверяем обработку ошибок в events_page."""
    with patch("src.views.load_transactions", side_effect=Exception("Test error")):
        result = events_page("2023-01-15", "M")
        assert "expenses" in result
        assert "income" in result
        assert isinstance(result["expenses"], dict)
        assert isinstance(result["income"], dict)
        assert result["expenses"].get("main", []) == []
        assert result["income"].get("main", []) == []
