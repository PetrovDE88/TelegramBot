from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                          f"{message.text},\n {bot.get_state(message.from_user.id)}")
