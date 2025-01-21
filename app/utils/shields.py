from datetime import datetime


def dday(target_date: datetime) -> int:
    current_date = datetime.now()
    return (target_date - current_date).days
