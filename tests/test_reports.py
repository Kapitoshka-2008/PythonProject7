import pytest
import pandas as pd
from datetime import datetime
from src.reports import spending_by_category, spending_by_weekday

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Дата операции": pd.to_datetime(["2023-01-01", "2023-01-15", "2023-02-01"]),
        "Категория": ["Еда", "Еда", "Транспорт"],
        "Сумма операции": [-1000, -500, -300],  # Траты — отрицательные значения!
        "Описание": ["Покупка", "Кафе", "Такси"]
    })

def test_spending_by_category(sample_dataframe):
    """Проверяем отчет по категориям."""
    result = spending_by_category(sample_dataframe, "Еда", "2023-02-01")
    assert result["total"] == 1500  # |-1000| + |-500|

def test_spending_by_weekday(sample_dataframe):
    """Проверяем средние траты по дням недели."""
    result = spending_by_weekday(sample_dataframe)
    assert "Sunday" in result  # 2023-01-01 и 2023-01-15 - воскресенья
    assert result["Sunday"] == 750.0  # (|1000| + |500|) / 2