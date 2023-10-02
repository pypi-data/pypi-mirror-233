import unittest
from datetime import datetime
from consistency_tracker import calculate_consistency  # Replace 'your_module' with your actual module name


class TestCalculateConsistency(unittest.TestCase):

    def test_calculate_consistency_empty_data(self):
        data = []
        result = calculate_consistency(data)
        self.assertEqual(result, [])

    def test_calculate_consistency_single_day_performed(self):
        data = [(1, datetime(2023, 1, 1))]
        result = calculate_consistency(data)
        self.assertEqual(result, [(1, datetime(2023, 1, 1))])

    def test_calculate_consistency_single_day_not_performed(self):
        data = [(0, datetime(2023, 1, 1))]
        result = calculate_consistency(data)
        self.assertEqual(result, [(0, datetime(2023, 1, 1))])

    def test_calculate_consistency_multiple_days_performed(self):
        data = [(1, datetime(2023, 1, 1)), (1, datetime(2023, 1, 2)),
                (1, datetime(2023, 1, 3)), (1, datetime(2023, 1, 4))]
        result = calculate_consistency(data)
        expected = [(1.0, datetime(2023, 1, 1)), (2.0, datetime(2023, 1, 2)),
                    (3.5, datetime(2023, 1, 3)), (5.5, datetime(2023, 1, 4))]
        self.assertEqual(result, expected)

    def test_calculate_consistency_multiple_days_with_skip(self):
        data = [(1, datetime(2023, 1, 1)), (0, datetime(2023, 1, 2)), (1, datetime(2023, 1, 3))]
        result = calculate_consistency(data)
        expected = [(1.0, datetime(2023, 1, 1)), (0.0, datetime(2023, 1, 2)), (1.0, datetime(2023, 1, 3))]
        self.assertEqual(result, expected)

    def test_calculate_consistency_multiple_days_restart(self):
        data = [(1, datetime(2023, 1, 1)), (0, datetime(2023, 1, 2)), (1, datetime(2023, 1, 3)),
                (1, datetime(2023, 1, 4)), (1, datetime(2023, 1, 5))]
        result = calculate_consistency(data)
        expected = [(1.0, datetime(2023, 1, 1)), (0.0, datetime(2023, 1, 2)), (1.0, datetime(2023, 1, 3)),
                    (2.0, datetime(2023, 1, 4)), (3.5, datetime(2023, 1, 5))]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
