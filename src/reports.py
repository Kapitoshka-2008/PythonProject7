import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)


def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца."""
    try:
        # Конвертируем дату, явно указывая формат
        if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
            transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%Y-%m-%d")

        date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
        start_date = date - pd.DateOffset(months=3)

        filtered = transactions[
            (transactions["Категория"] == category) &
            (transactions["Дата операции"] >= start_date) &
            (transactions["Дата операции"] <= date)
            ]

        return {"total": filtered["Сумма платежа"].sum()}

    except Exception as e:
        logging.error(f"Ошибка генерации отчета по категории: {e}")
        raise


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """Средние траты по дням недели."""
    try:
        # Проверяем, что DataFrame не пустой
        if transactions.empty:
            logging.warning("Получен пустой DataFrame")
            return {}
            
        # Проверяем наличие необходимых колонок
        required_columns = ["Дата операции", "Сумма платежа"]
        if not all(col in transactions.columns for col in required_columns):
            logging.error(f"Отсутствуют необходимые колонки. Требуются: {required_columns}")
            return {}
            
        # Проверяем, что даты уже в формате datetime
        if not pd.api.types.is_datetime64_any_dtype(transactions["Дата операции"]):
            # Если даты в виде строк, пробуем преобразовать их
            try:
                # Сначала пробуем стандартный формат
                transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
            except Exception as e:
                logging.error(f"Ошибка преобразования даты: {e}")
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
            logging.warning("Нет данных после фильтрации.")
            return {}

        # Вычисляем день недели
        filtered["weekday"] = filtered["Дата операции"].dt.day_name()

        # Агрегируем данные по дням недели
        grouped = filtered.groupby("weekday")["Сумма платежа"].mean()

        # Получаем результат в виде словаря
        result = grouped.to_dict()

        # Проверка результата
        if not result:
            logging.warning("Не удалось сформировать отчет по дням недели.")

        return result

    except Exception as e:
        logging.error(f"Ошибка генерации отчета по дням недели: {e}")
        return {}