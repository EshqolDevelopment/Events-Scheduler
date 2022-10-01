from datetime import datetime


def reformat_date(date: datetime.date):
    return date.strftime("%d/%m/%Y")


def reformat_time(time_: datetime.time):
    return time_.strftime("%H:%M:%S")


def reformat_extend_date(next_run_time: datetime) -> str:
    return next_run_time.strftime("Date: %d/%m/%Y | Time: %H:%M")
