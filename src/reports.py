import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable
import logging
import functools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_report_errors(func: Callable) -> Callable:
    """Декоратор для обработки ошибок в функциях отчетов."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка в функции {func.__name__}: {e}")
            if func.__name__ == "spending_by_category":
                return {"total": 0.0}
            if func.__name__ == "spending_by_weekday":
                return {}
            return {}
    return wrapper

@handle_report_errors
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца."""
    # Проверяем входные данные
    if transactions.empty:
        logger.warning("Получен пустой DataFrame")
        return {"total": 0.0}
        
    if not category:
        logger.warning("Не указана категория")
        return {"total": 0.0}

    # Конвертируем дату, явно указывая формат
    if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%Y-%m-%d")

    # Устанавливаем дату для фильтрации
    date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
    start_date = date - pd.DateOffset(months=3)

    # Фильтруем транзакции
    filtered = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= date)
    ]

    # Проверяем наличие данных после фильтрации
    if filtered.empty:
        logger.warning(f"Нет данных по категории {category} за указанный период")
        return {"total": 0.0}

    # Считаем сумму трат
    total = filtered[filtered["Сумма операции"] < 0]["Сумма операции"].sum()
    
    logger.info(f"Рассчитана сумма трат по категории {category}: {abs(total)}")
    return {"total": abs(total)}

@handle_report_errors
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """Средние траты по дням недели."""
    # Проверяем входные данные
    if transactions.empty:
        logger.warning("Получен пустой DataFrame")
        return {}
        
    # Проверяем наличие необходимых колонок
    required_columns = ["Дата операции", "Сумма операции"]
    if not all(col in transactions.columns for col in required_columns):
        logger.error(f"Отсутствуют необходимые колонки. Требуются: {required_columns}")
        return {}
        
    # Проверяем, что даты уже в формате datetime
    if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
        try:
            transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
        except Exception as e:
            logger.error(f"Ошибка преобразования даты: {e}")
            return {}

    # Фильтруем транзакции только если указана дата
    filtered = transactions
    if date:
        date = pd.to_datetime(date)
        start_date = date - pd.DateOffset(months=3)
        filtered = transactions[
            (transactions["Дата операции"] >= start_date) &
            (transactions["Дата операции"] <= date)
        ]

    # Проверка наличия данных после фильтрации
    if filtered.empty:
        logger.warning("Нет данных после фильтрации")
        return {}

    # Фильтруем только траты (отрицательные суммы)
    spending_transactions = filtered[filtered["Сумма операции"] < 0].copy()

    if spending_transactions.empty:
        logger.warning("Нет данных о тратах после фильтрации")
        return {}

    # Вычисляем день недели
    spending_transactions["weekday"] = spending_transactions["Дата операции"].dt.day_name()
    # Берем абсолютные значения трат для расчета среднего
    spending_transactions["Сумма операции"] = spending_transactions["Сумма операции"].abs()

    # Агрегируем данные по дням недели
    grouped = spending_transactions.groupby("weekday")["Сумма операции"].mean()

    # Получаем результат в виде словаря
    result = grouped.to_dict()

    # Проверка результата
    if not result:
        logger.warning("Не удалось сформировать отчет по дням недели")
        return {}

    logger.info(f"Сформирован отчет по дням недели: {result}")
    return result