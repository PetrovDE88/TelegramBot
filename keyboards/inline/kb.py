from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import datetime
from typing import Any, Callable


def cites_markup(cities: dict) -> InlineKeyboardMarkup:
    """
    Создание кнопок выбора города
    :param cities: dict - словарь со списков подходящих городов из парсинга
    :return: keyboard: InlineKeyboardMarkup - кнопки выбора города
    """
    keyboard = InlineKeyboardMarkup()
    for city in cities.keys():
        keyboard.add(InlineKeyboardButton(text=city, callback_data=city+';keycity'))
    return keyboard


def calendar_create(min_date: datetime) -> Any:
    result, step = DetailedTelegramCalendar(locale='ru', min_date=min_date).build()
    return result, step


def calendar_process(min_date: datetime, call: Callable) -> Any:
    result, key, step = DetailedTelegramCalendar(locale='ru', min_date=min_date).process(call)
    return result, key, step
