import unittest
from datetime import datetime, time
from utils_funcions import *


class TestFindAvailableTimes(unittest.TestCase):
	def setUp(self):
		self.trainer_schedule = [
			{"date": datetime(2025, 1, 5).date(), "start_time": time(9, 0), "end_time": time(17, 0)}
		]
		self.service_durations = {1: 60}

	def test_no_bookings(self):
		bookings = []
		current_date = datetime(2025, 1, 5).date()
		expected = [(time(9, 0), time(17, 0))]
		result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
		self.assertEqual(result, expected)

	def test_full_day_booked(self):
		bookings = [
			{"datetime_start": datetime(2025, 1, 5, 9, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 10, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 12, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 13, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 15, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 16, 0), "service_id": 1},
		]
		current_date = datetime(2025, 1, 5).date()
		expected = []
		result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
		self.assertEqual(result, expected)

	def test_partial_availability(self):
		bookings = [
			{"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
		]
		current_date = datetime(2025, 1, 5).date()
		expected = [
			(time(9, 0), time(11, 0)),
			(time(12, 0), time(14, 0)),
			(time(15, 0), time(17, 0)),
		]
		result = find_available_times(self.trainer_schedule, bookings, current_date, self.service_durations)
		self.assertEqual(result, expected)

	def test_no_schedule_for_date(self):
		trainer_schedule = [
			{"date": datetime(2025, 1, 6).date(), "start_time": time(9, 0), "end_time": time(17, 0)}
		]
		bookings = [
			{"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
		]
		current_date = datetime(2025, 1, 5).date()
		expected = []
		result = find_available_times(trainer_schedule, bookings, current_date, self.service_durations)
		self.assertEqual(result, expected)

	def test_multiple_services_with_different_durations(self):
		service_durations = {1: 60, 2: 30}
		bookings = [
			{"datetime_start": datetime(2025, 1, 5, 10, 0), "service_id": 1},
			{"datetime_start": datetime(2025, 1, 5, 12, 0), "service_id": 2},
		]
		current_date = datetime(2025, 1, 5).date()
		expected = [
			(time(9, 0), time(10, 0)),
			(time(11, 0), time(12, 0)),
			(time(12, 30), time(17, 0)),
		]
		result = find_available_times(self.trainer_schedule, bookings, current_date, service_durations)
		self.assertEqual(result, expected)


if __name__ == "__main__":
	unittest.main()
