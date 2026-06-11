import pytest
from main import calculate_total_revenue


def test_booked_and_cancelled():
    ticket_list = [
        {"price": 500, "status": "Booked"},
        {"price": 300, "status": "Cancelled"},
        {"price": 700, "status": "Booked"}
    ]

    assert calculate_total_revenue(ticket_list) == 1200.0


def test_empty_list():
    assert calculate_total_revenue([]) == 0.0
