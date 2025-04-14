import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, mock_open
from src.utils import load_transactions, filter_transactions_by_date


# Фикстура с тестовыми данными Excel (в формате CSV для упрощения)
@pytest.fixture
def mock_excel_data():
    return """
Дата операции,Сумма платежа,Категория
2023-01-01,1000,Еда
2023-01-15,-500,Транспорт
2023-02-01,2000,Зарплата
"""


# Тест для загрузки транзакций
@patch("pandas.read_excel")
def test_load_transactions_success(mock_read_excel):
    """Проверяем загрузку данных из Excel."""
    # Мокируем возвращаемый DataFrame
    mock_df = pd.DataFrame({
        "Дата операции": ["2023-01-01", "2023-01-15"],
        "Сумма платежа": [1000, -500],
        "Категория": ["Еда", "Транспорт"]
    })
    mock_read_excel.return_value = mock_df

    # Вызываем функцию
    result = load_transactions("fake_path.xlsx")

    # Проверяем, что данные загружены корректно
    assert not result.empty
    assert "Дата операции" in result.columns
    assert mock_read_excel.called


@patch("pandas.read_excel")
def test_load_transactions_file_not_found(mock_read_excel):
    """Проверяем обработку ошибки при загрузке файла."""
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
    with pytest.raises(Exception, match="Ошибка загрузки данных"):
        load_transactions("invalid_path.xlsx")


# Тест для фильтрации по дате
def test_filter_transactions_by_date():
    """Проверяем фильтрацию транзакций по периоду."""
    # Создаем тестовый DataFrame
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2023-01-01", "2023-01-15", "2023-02-01"]),
        "Сумма платежа": [1000, -500, 2000]
    })

    # Фильтруем за январь 2023
    result = filter_transactions_by_date(df, "2023-01-20", "M")

    # Проверяем, что остались только январские транзакции
    assert len(result) == 2
    assert all(result["Дата операции"].dt.month == 1)


def test_filter_transactions_invalid_period():
    """Проверяем обработку некорректного периода."""
    df = pd.DataFrame({"Дата операции": []})
    with pytest.raises(ValueError, match="Неподдерживаемый период"):
        filter_transactions_by_date(df, "2023-01-01", "INVALID")