import unittest
from utils_funcions import *


class TestFindAvailableTimes(unittest.TestCase):
    def setUp(self):
        self.trainer_schedule = [
            {"date": datetime(2025, 6, 15).date(), "start_time": time(7, 0), "end_time": time(20, 0)}
        ]
        self.service_durations = {1: 120, 2: 90}

    def test_no_bookings(self):
        bookings = []
        current_date = datetime(2025, 6, 15).date()
        expected = [(time(7, 0), time(20, 0))]
        result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
        self.assertEqual(result, expected)

    def test_single_booking(self):
        bookings = [
            {"datetime_start": datetime(2025, 6, 15, 8, 0), "service_id": 1}
        ]
        current_date = datetime(2025, 6, 15).date()
        expected = [(time(7, 0), time(8, 0)), (time(10, 0), time(20, 0))]
        result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
        self.assertEqual(result, expected)

    def test_multiple_bookings(self):
        bookings = [
            {"datetime_start": datetime(2025, 6, 15, 8, 0), "service_id": 1},
            {"datetime_start": datetime(2025, 6, 15, 12, 0), "service_id": 2},
            {"datetime_start": datetime(2025, 6, 15, 18, 0), "service_id": 1}
        ]
        current_date = datetime(2025, 6, 15).date()
        expected = [
            (time(7, 0), time(8, 0)),
            (time(10, 0), time(12, 0)),
            (time(13, 30), time(18, 0))
        ]
        result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
        self.assertEqual(result, expected)

    def test_no_schedule_for_date(self):
        bookings = [
            {"datetime_start": datetime(2025, 6, 15, 8, 0), "service_id": 1}
        ]
        current_date = datetime(2025, 6, 16).date()
        expected = []
        result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
        self.assertEqual(result, expected)

    def test_partial_overlap_booking(self):
        bookings = [
            {"datetime_start": datetime(2025, 6, 15, 9, 30), "service_id": 2}
        ]
        current_date = datetime(2025, 6, 15).date()
        expected = [(time(7, 0), time(9, 30)), (time(11, 0), time(20, 0))]
        result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
