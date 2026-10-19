import datetime

import jdatetime
from django.utils import timezone

_PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
_TO_ENGLISH_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def to_persian_digits(value):
    return str(value).translate(_PERSIAN_DIGITS)


def to_english_digits(value):
    return str(value).translate(_TO_ENGLISH_DIGITS)


def as_jalali(value):
    if not value:
        return None
    if isinstance(value, jdatetime.datetime):
        return value
    if isinstance(value, jdatetime.date):
        return value
    if isinstance(value, datetime.datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return jdatetime.datetime.fromgregorian(datetime=value.replace(tzinfo=None))
    if isinstance(value, datetime.date):
        return jdatetime.date.fromgregorian(date=value)
    return None


def format_jalali(value, with_time=False):
    converted = as_jalali(value)
    if converted is None:
        return ''
    month = jdatetime.date.j_months_fa[converted.month - 1]
    text = f'{converted.day} {month} {converted.year}'
    if with_time and isinstance(converted, jdatetime.datetime):
        text = f'{text}، {converted.hour:02d}:{converted.minute:02d}'
    return to_persian_digits(text)


def format_jalali_input(value):
    converted = as_jalali(value)
    if converted is None:
        return ''
    return to_persian_digits(f'{converted.year}/{converted.month:02d}/{converted.day:02d}')


def parse_jalali_date(value):
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date) and not isinstance(value, jdatetime.date):
        return value
    if isinstance(value, jdatetime.date):
        return value.togregorian()

    text = to_english_digits(value).strip()
    text = text.replace('-', '/').replace('.', '/').replace('\\', '/')
    parts = [part.strip() for part in text.split('/') if part.strip()]
    if len(parts) != 3:
        raise ValueError('invalid jalali date')

    year, month, day = (int(part) for part in parts)
    if year < 100 and day > 1300:
        year, day = day, year
    if year < 1700:
        return jdatetime.date(year, month, day).togregorian()
    return datetime.date(year, month, day)
