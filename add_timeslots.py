# add_timeslots.py
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_mary.settings')
django.setup()

from core.models import TimeSlot

def add_timeslots():
    # Очистка существующих слотов (опционально)
    TimeSlot.objects.all().delete()

    # Начальная дата
    start_date = datetime(2025, 9, 4, 17, 30)  # 04.09.2025 17:30

    # Список слотов
    slots = [
        {"day": 4, "times": ["17:30"]},
        {"day": 5, "times": ["17:30", "19:30"]},
        {"day": 6, "times": ["11:00", "15:00"]},
        {"day": 11, "times": ["17:30"]},
        {"day": 12, "times": ["19:30"]},
        {"day": 13, "times": ["11:00", "13:00"]},
        {"day": 16, "times": ["17:30"]},
        {"day": 17, "times": ["17:30"]},
        {"day": 19, "times": ["17:30", "19:30"]},
        {"day": 20, "times": ["11:00", "13:00", "17:30"]},
        {"day": 22, "times": ["17:30"]},
        {"day": 23, "times": ["17:30"]},
        {"day": 24, "times": ["17:30"]},
        {"day": 25, "times": ["17:30"]},
        {"day": 26, "times": ["17:30"]},
        {"day": 27, "times": ["15:00", "17:00"]},
        {"day": 29, "times": ["17:30"]},
        {"day": 30, "times": ["17:30"]},
    ]

    for slot in slots:
        day = slot["day"]
        times = slot["times"]
        for time_str in times:
            hour, minute = map(int, time_str.split(':'))
            date_time = datetime(2025, 9, day, hour, minute)
            TimeSlot.objects.create(date_time=date_time, is_booked=False)

if __name__ == "__main__":
    add_timeslots()
    print("Слоты времени успешно добавлены!")
