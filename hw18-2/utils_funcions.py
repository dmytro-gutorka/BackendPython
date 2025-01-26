from datetime import datetime, timedelta, time
from typing import List, Dict, Tuple

Schedule = List[Dict[str, object]]
Booking = Dict[str, object]


def find_available_times(
		trainer_schedule: Schedule,
		bookings: List[Booking],
		current_date: datetime.date,
		service_durations: Dict[int, int]
) -> List[Tuple[time, time]]:
	schedule_intervals = [
		(entry["start_time"], entry["end_time"])
		for entry in trainer_schedule
		if entry["date"] == current_date
	]

	booking_intervals = []
	for booking in bookings:
		if booking["datetime_start"].date() == current_date:
			service_id = booking["service_id"]
			duration = timedelta(minutes=service_durations.get(service_id, 0))
			booking_intervals.append((
				booking["datetime_start"].time(),
				(booking["datetime_start"] + duration).time()
			))

	booking_intervals.sort(key=lambda x: x[0])

	# Поиск доступных интервалов
	available_intervals = []
	for start_time, end_time in schedule_intervals:
		current_start = start_time
		for booking_start, booking_end in booking_intervals:
			if booking_start <= current_start < booking_end:
				# Если текущее время занято, обновляем его
				current_start = booking_end
			elif current_start < booking_start <= end_time:
				# Добавляем интервал до следующего бронирования
				available_intervals.append((current_start, booking_start))
				current_start = booking_end
		if current_start < end_time:
			# Добавляем оставшийся интервал до конца расписания
			available_intervals.append((current_start, end_time))

	return available_intervals


trainer_schedule = [
	{"date": datetime(2025, 1, 5).date(), "start_time": time(9, 0), "end_time": time(17, 0)}
]
bookings = [
	{"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1},
	{"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1},
	{"datetime_start": datetime(2025, 1, 5, 16, 30), "service_id": 1}
]
service_durations = {1: 60}
current_date = datetime(2025, 1, 5).date()


available_times = find_available_times(trainer_schedule, bookings, current_date, service_durations)
print(available_times)
