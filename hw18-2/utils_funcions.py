from datetime import datetime, time, timedelta
from typing import List, Dict, Tuple


def find_available_times(
        trainer_schedule: List[Dict[str, object]],
        bookings: List[Dict[str, object]],
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

    available_intervals = []
    for start_time, end_time in schedule_intervals:
        current_start = start_time
        for booking_start, booking_end in booking_intervals:
            if booking_start <= current_start < booking_end:
                current_start = booking_end
            elif current_start < booking_start <= end_time:
                available_intervals.append((current_start, booking_start))
                current_start = booking_end
        if current_start < end_time:
            if current_start != end_time:
                available_intervals.append((current_start, end_time))

    return available_intervals