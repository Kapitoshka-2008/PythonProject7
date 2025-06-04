"""Test views module."""

import pytest

from src.views import filter_transactions_by_date


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    return [
        {
            "Дата операции": "2024-01-01",
            "Сумма операции": 100.0,
            "Категория": "Food",
            "Описание": "Grocery shopping"
        },
        {
            "Дата операции": "2024-01-02",
            "Сумма операции": 200.0,
            "Категория": "Transport",
            "Описание": "Taxi"
        }
    ]


def test_filter_transactions_by_date(sample_transactions):
    """Test filtering transactions by date."""
    start_date = "2024-01-01"
    end_date = "2024-01-01"
    filtered = filter_transactions_by_date(sample_transactions, start_date, end_date)
    assert len(filtered) == 1
    assert filtered[0]["Дата операции"] == "2024-01-01"


def test_filter_transactions_by_date_no_dates(sample_transactions):
    """Test filtering transactions with no date range."""
    filtered = filter_transactions_by_date(sample_transactions)
    assert len(filtered) == len(sample_transactions)


def test_filter_transactions_by_date_invalid_dates(sample_transactions):
    """Test filtering transactions with invalid dates."""
    filtered = filter_transactions_by_date(sample_transactions, "invalid", "invalid")
    assert len(filtered) == len(sample_transactions)


def test_main_page(client, sample_transactions):
    """Test main page route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Finance Analyzer" in response.data


def test_events_page(client, sample_transactions):
    """Test events page route."""
    response = client.get("/events")
    assert response.status_code == 200
    assert b"Events" in response.data


def test_main_page_with_transactions(client, sample_transactions):
    """Test main page with transaction data."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Transaction History" in response.data


def test_events_page_with_transactions(client, sample_transactions):
    """Test events page with transaction data."""
    response = client.get("/events")
    assert response.status_code == 200
    assert b"Event Analysis" in response.data


def test_main_page_with_empty_transactions(client):
    """Test main page with empty transaction data."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"No transactions found" in response.data


def test_events_page_with_empty_transactions(client):
    """Test events page with empty transaction data."""
    response = client.get("/events")
    assert response.status_code == 200
    assert b"No events found" in response.data


def test_main_page_with_invalid_date_filter(client, sample_transactions):
    """Test main page with invalid date filter."""
    response = client.get("/?start_date=invalid&end_date=invalid")
    assert response.status_code == 200
    assert b"Invalid date format" in response.data


def test_events_page_with_invalid_date_filter(client, sample_transactions):
    """Test events page with invalid date filter."""
    response = client.get(
        "/events?start_date=invalid&end_date=invalid"
    )
    assert response.status_code == 200
    assert b"Invalid date format" in response.data
