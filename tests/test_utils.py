"""Tests for utility functions."""
from datetime import datetime

import pytest

from src.utils import get_greeting


def test_get_greeting():
    """Test greeting generation for different times of day."""
    test_cases = [
        (datetime(2023, 1, 1, 7, 0), "Доброе утро"),
        (datetime(2023, 1, 1, 13, 0), "Добрый день"),
        (datetime(2023, 1, 1, 18, 0), "Добрый вечер"),
        (datetime(2023, 1, 1, 2, 0), "Доброй ночи"),
    ]

    for time, expected in test_cases:
        assert get_greeting(time) == expected