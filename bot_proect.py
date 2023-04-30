import telebot
import sqlite3
from pytube import YouTube
import random
from telebot import types
from selenium import webdriver
import time
from youtubesearchpython import VideosSearch

bot = telebot.TeleBot('5985465061:AAETA8s7EmCFF96eDJfQwEQSlENTArm3lak')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Привет")
    btn2 = types.KeyboardButton("🎥 Найти клип")
    btn3 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я помогу тебе найти нужный клип".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, text="{0.first_name}! Я помогу тебе разобраться с управлением и выяснить в чем проблема.".format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, text="Если вы здесь, потому что не знаете как работает бот, вам сюда 👉🏻 /control")
    bot.send_message(message.chat.id, text="Если у вас не загружается видео, вам сюда 👉 /error")

@bot.message_handler(commands=['control'])
def control(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     text="{0.first_name}! Я помогу тебе разобраться с управлением".format(
                         message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id,
                     text="Я могу найти вам клип по названию, когда вы выберите              👉 🎥 Найти клип 👉 Найти по названию 👉 и введете название")
    bot.send_message(message.chat.id,
                     text="Также я могу посоветовать вам клип из своих запасов, для этого выберите 👉 🎥 Найти клип 👉 Клип на выбор бота 👉 и подождите")

@bot.message_handler(commands=['error'])
def error(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     text="{0.first_name}! Если у вас не загружается видео, то можно попробовать это исправить тем, что 👉".format(
                         message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id,
                     text="1 - Попробовать скачать видео снова")
    bot.send_message(message.chat.id,
                     text="2 - Попробовать скачать видео через некоторое время")
    bot.send_message(message.chat.id,
                     text="Если видео всё равно не скачалось, то скорее всего это из-за ограничений по возрасту, "
                          "слишком большого размера или видео устарело и YouTube его больше не поддерживает.😞 "
                          "Поэтому попробуйте скачать что-нибудь другое...")

@bot.message_handler(content_types=['text'])
def inline_key(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, 'Привет!))')
    elif message.text == "👋 Привет":
        bot.send_message(message.chat.id, text="Привеееет. Рад вас видеть)")
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как тебя зовут?")
        btn2 = types.KeyboardButton("Что ты можешь?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    elif message.text == "🎥 Найти клип":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Найти по названию")
        btn2 = types.KeyboardButton("Клип на выбор бота")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выбери действие", reply_markup=markup)

    elif message.text == "Как тебя зовут?":
        bot.send_message(message.chat.id, "У меня нет имени....")

    elif message.text == "Что ты можешь?":
        bot.send_message(message.chat.id, text="Могу найти вам определенный клип, а могу порекомендовать свой😜")

    elif message.text == "Найти по названию":
        sm = bot.send_message(message.chat.id, "Введите название клипа, которую хотите найти")
        bot.register_next_step_handler(sm, search)

    elif message.text == "Клип на выбор бота":
        bot.send_message(message.chat.id, "Подождите немного...")
        time.sleep(3)
        sqlite_connection = sqlite3.connect('MyDB3.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT * from links"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        row = random.choice(records)
        #bot.send_message(message.chat.id, row[1])
        downloaded = False
        while not downloaded:
            try:
                row = random.choice(records)
                downloading(row[1], message)
                downloaded = True
            except:
                print("Error", row[1])


    elif message.text == "Вернуться в главное меню":
        returned(message)

    else:
        bot.send_message(message.chat.id, text="К сожалению я вас не понял, повторите пожалуйста((....")

def returned(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("👋 Привет")
    button2 = types.KeyboardButton("🎥 Найти клип")
    button3 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=markup)


def search(message):
    # video_href = "https://www.youtube.com/results?search_query=" + message.text
    # driver.get(video_href)
    # sleep(2)
    # videos = driver.find_elements(by="video-title")
    result = VideosSearch(message.text, limit = 1).result()
    for i in range(len(result["result"])):
        try:
            bot.send_message(message.chat.id, "Скачиваем..."+ result["result"][i]["link"])
            downloading(result["result"][i]["link"], message)
        except:
            bot.send_message(message.chat.id, "Не получилось скачать...😢")
            bot.send_message(message.chat.id, "Чтобы узнать проблему попробуйте команду /help")
            returned(message)
        #bot.send_message(message.chat.id, videos[i].get_attribute("href"))
        #print(result["result"][i]["link"])
        # bot.send_message(message.chat.id, result["result"][i]["link"])
        #if i == 1:
        #    break

def downloading(link, message):
    my_video = YouTube(link)
    path = my_video.streams.get_highest_resolution().download()
    video = open(path, 'rb')
    #print(path)
    bot.send_video(message.chat.id, video)
    bot.send_message(message.chat.id, f"Успешно скачан.....")


bot.polling()
