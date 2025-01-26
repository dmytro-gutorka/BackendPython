from datetime import datetime, timedelta, time
from typing import List, Dict, Tuple

# Определение типов для ясности
Schedule = List[Dict[str, object]]
Booking = Dict[str, object]


# Оптимизированная функция
def find_available_times(
		trainer_schedule: Schedule,
		bookings: List[Booking],
		current_date: datetime.date,
		service_durations: Dict[int, int]
) -> List[Tuple[time, time]]:
	"""
	Находит доступные интервалы времени на основании расписания и бронирований.

	Args:
		trainer_schedule: Список расписаний тренера.
		bookings: Список бронирований.
		current_date: Дата, для которой ищутся доступные интервалы.
		service_durations: Словарь с длительностью услуг по их ID.

	Returns:
		Список доступных временных интервалов (начало, конец).
	"""
	# Извлечение интервалов расписания для текущей даты
	schedule_intervals = [
		(entry["start_time"], entry["end_time"])
		for entry in trainer_schedule
		if entry["date"] == current_date
	]

	# Создание списка интервалов бронирования
	booking_intervals = []
	for booking in bookings:
		if booking["datetime_start"].date() == current_date:
			service_id = booking["service_id"]
			duration = timedelta(minutes=service_durations.get(service_id, 0))
			booking_intervals.append((
				booking["datetime_start"].time(),
				(booking["datetime_start"] + duration).time()
			))

	# Сортировка интервалов бронирования по началу времени
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


# Пример использования
trainer_schedule = [
	{"date": datetime(2025, 6, 15).date(), "start_time": time(7, 0), "end_time": time(20, 0)}
]
bookings = [
	{"datetime_start": datetime(2025, 6, 15, 8, 0), "service_id": 1},
	{"datetime_start": datetime(2025, 6, 15, 12, 0), "service_id": 1},
	{"datetime_start": datetime(2025, 6, 15, 18, 0), "service_id": 1}
]
service_durations = {1: 120}
current_date = datetime(2025, 6, 15).date()

# Результат
available_times = find_available_times(trainer_schedule, bookings, current_date, service_durations)
print(available_times)
