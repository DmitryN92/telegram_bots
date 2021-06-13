# удачный работающий вариант

import telebot
import config
import random
import os

from telebot import types

bot = telebot.TeleBot(config.TG_TOKEN)
SECRET_FLAG = False # для скрытого режима работы

myphotos = os.listdir(r'telegram.photos')
photo_alina = os.listdir(r'telegram.alina_photos')


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open(r'telegram.stickers\sticker_homer.webp','rb')
    bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Случайное фото")
    #item2 = types.KeyboardButton("Как дела?")

    markup.add(item1)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n"
                                      "Я - <b>{1.first_name}</b>, бот созданный,"
                                      " чтобы вызывать ностальгию.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def lalala(message):
    global SECRET_FLAG
    global photo_alina

    if message.chat.type == 'private':
        if message.text == 'Пэмадий':
            SECRET_FLAG = True
            bot.send_message(message.chat.id, 'Алина, секретный режим работы активирован')

        if SECRET_FLAG and (message.text == 'Случайное фото'):
            num = random.randint(0, len(photo_alina))
            myphoto = photo_alina[num]
            photo_file = open('telegram.alina_photos\\%s' % myphoto, 'rb')
            bot.send_photo(message.chat.id, photo_file)


        if not SECRET_FLAG and (message.text == 'Случайное фото'):
            num = random.randint(0, len(myphotos)-1)
            myphoto = myphotos[num]
            photo_file = open('telegram.photos\\%s' % myphoto, 'rb')
            bot.send_photo(message.chat.id, photo_file)
        elif not SECRET_FLAG:
            bot.send_message(message.chat.id, 'Я не знаю что ответить :(')



bot.polling(none_stop=True)