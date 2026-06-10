import unittest
from main import calculate_total_revenue


class TestRevenue(unittest.TestCase):

    def test_booked_and_cancelled(self):
        ticket_list = [
            {"price": 500, "status": "Booked"},
            {"price": 300, "status": "Cancelled"},
            {"price": 700, "status": "Booked"}
        ]

        self.assertEqual(calculate_total_revenue(ticket_list), 1200.0)

    def test_empty_list(self):
        self.assertEqual(calculate_total_revenue([]), 0.0)


if __name__ == "__main__":
    unittest.main()