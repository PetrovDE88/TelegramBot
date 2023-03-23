from telebot.types import Message
from states.input_data_state import UserState
from loader import bot
from utils.api_hotes import get_cites
from keyboards.inline import kb
from telebot import custom_filters


@bot.message_handler(commands=['lowprice' , 'highprice', 'bestdeal'])
def first_command(message: Message) -> None:
    """
    Функция запрашивающая город для поиска
    """
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'В каком городе будем искать отель?')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['first_command'] = message.text

@bot.message_handler(state=UserState.city)
def get_city(message: Message) -> None:
    """
    Вывод кнопок уточнения города

    """
    cities: dict | None = get_cites(message.text)
    if cities is None:
        bot.send_message(message.from_user.id, f'Ресурс недоступен, попробуйте позже.')
#TODO Добавить обработку ошибок парсинга
    else:
        bot.set_state(message.from_user.id, UserState.city_confirm, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = cities
        bot.send_message(message.from_user.id, 'Уточните город', reply_markup=kb.cites_markup(cities=cities))
    ...

@bot.message_handler(state=UserState.number_of_hotels)
def num_hotels(message: Message) -> None:
    """
    Запрос количества отелей для вывода

    """
    if message.text.isdigit():
        k = int(message.text)
        if (0 < k) and (k <= 5):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotels_num'] = k
            bot.set_state(message.from_user.id, UserState.number_of_photos)
            bot.send_message(message.from_user.id, 'Количество фото отеля (не более 5, 0 - если не нужно):')
        else:
            bot.send_message(message.from_user.id, 'Не более 5')
    else:
        bot.send_message(message.from_user.id, 'Необходимо указать цифры')

@bot.message_handler(state=UserState.number_of_photos)
def num_photos(message: Message) -> None:
    """
    Запрос количества фото для вывода

    """
    if message.text.isdigit():
        k = int(message.text)
        if (0 < k) and (k <= 5):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['photos_num'] = k
            sendinfo(message)

        else:
            bot.send_message(message.from_user.id, 'Не более 5')
    else:
        bot.send_message(message.from_user.id, 'Необходимо указать цифры')


def sendinfo(message: Message) -> None:
    """
    Отправка информации пользователю о выбранной информации
    TODO Сюда добавить обработку информации при запросе bestdeal
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        text = f'Текущий город: {data["city"]}\n' \
               f'Даты проживания: {data["check_in"]} - {data["check_out"]}\n' \
               f'Количество отелей в выборке: {data["hotels_num"]}\n' \
               f'Количество фото отелей: {data["photos_num"]}'
    bot.send_message(message.from_user.id, text)


bot.add_custom_filter(custom_filters.StateFilter(bot))