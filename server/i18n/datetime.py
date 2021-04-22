import datetime as dt

from babel.dates import format_date

from .locale import Locale


def dateformat(d: dt.datetime) -> str:
    locale = Locale.get()
    return format_date(d, locale=locale, format="long")
