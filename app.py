import telebot
from config import TOKEN, curr
from extensions import APIException, Conversion


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для конвертации валюты введите сообщение в следующем формате:\n <конвертируемая валюта>\
<валюта, в которую нужно перевести><количество конвертируемой валюты>\n \
Например, чтобы узнать стоимость 10 долларов в рублях, нужно ввести: доллар рубль 10\n \
Список всех валют можно увидеть по команде /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in curr.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split()

        if len(value) != 3:
            raise APIException('Неверное количество параметров.\n '
                               'Инструкцию по вводу можно увидеть по команде /help')

        base, quote, amount = value
        base = base.lower()
        quote = quote.lower()
        total_quote = Conversion.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        text = f'Цена {amount} {base} составляет {round(total_quote, 2)} {quote}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
