from telebot.types import CallbackQuery
from keyboards.inline import kb
from states.input_data_state import UserState
from loader import bot
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta


@bot.callback_query_handler(func=lambda call: call.data.endswith('keycity'))
def city_conf(call: CallbackQuery) -> None:

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        cities = data['city']
        data['city'] = call.data.split(';')[0]
        data['city_id'] = cities.get(data['city'])
        bot.send_message(call.from_user.id, f"{data['city']} - {data['city_id']}")

    bot.set_state(call.from_user.id, UserState.check_in, call.message.chat.id)
    bot.send_message(call.from_user.id, f'Дата заезда:', reply_markup=kb.calendar_create(date.today()))


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=UserState.check_in)
def in_calc(c) -> None:
    user_id = chat_id = c.message.chat.id
    result, key, step = kb.calendar_process(date.today(), c.data)
    if not result and key:
        bot.edit_message_text(f"Дата заезда:",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id, chat_id) as data:
            data['check_in'] = result

        bot.edit_message_text(f"Выбранная дата заезда: {result}",
                              c.message.chat.id,
                              c.message.message_id)

        bot.set_state(user_id, UserState.check_out, chat_id)
        bot.send_message(chat_id, 'Дата выезда:', reply_markup=kb.calendar_create(data['check_in']))


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=UserState.check_out)
def out_cal(c) -> None:
    user_id = chat_id = c.message.chat.id
    with bot.retrieve_data(user_id, chat_id) as data:
        check_in_date = data['check_in'] + timedelta(days=1)
    result, key, step = kb.calendar_process(check_in_date, c.data)
    if not result and key:
        bot.edit_message_text(f"Дата выезда:",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id, chat_id) as data:
            data['check_out'] = result

        bot.edit_message_text(f"Выбранная дата выезда: {result}",
                              c.message.chat.id,
                              c.message.message_id)

        bot.set_state(user_id, UserState.number_of_hotels, chat_id)
        bot.send_message(chat_id, 'Какое количество отелей выбрать (не более 5)?')



