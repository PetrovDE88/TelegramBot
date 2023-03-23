from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    city = State()
    city_confirm = State()
    check_in = State()
    check_out = State()
    number_of_hotels = State()
    number_of_photos = State()
    confim_info = State()
    min_price = State()
    max_price = State()
    distance = State()
