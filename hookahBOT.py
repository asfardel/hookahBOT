import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
import requests

API_TOKEN = '7367410479:AAG2lm0_YWlbtry9enSf2Z7Bpd7maqSdXtg'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton('перечная мята')
    button2 = KeyboardButton('Опция 2')
    button3 = KeyboardButton('Опция 3')
    markup.add(button1, button2, button3)
    
    bot.send_message(message.chat.id, "Добро пожаловать! Пожалуйста, выберите одну из опций:", reply_markup=markup)

# Обработчик нажатий кнопок
@bot.message_handler(func=lambda message: message.text in ['перечная мята', 'Опция 2', 'Опция 3'])
def handle_option(message):
    if message.text == 'перечная мята':
        bot.send_message(message.chat.id, "Вы выбрали Опцию 1!")
        photo_path = r"C:\Users\vika0\zxc\photo\photo_2024-06-12_19-56-34.jpg"
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    elif message.text == 'Опция 2':
        bot.send_message(message.chat.id, "Вы выбрали Опцию пошеssssл нахуй!")
        photo_path = r"C:\Users\vika0\zxc\photo\photo_2024-06-12_19-56-34.jpg"
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    elif message.text == 'Опция 3':
        bot.send_message(message.chat.id, "Вы выбрали Опцию 3!")
        photo_path = r"C:\Users\vika0\zxc\photo\photo_2024-06-12_19-56-34.jpg"
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

# Запуск бота с увеличенным таймаутом и механизмом повторных попыток
while True:
    try:
        bot.polling(timeout=60, long_polling_timeout=60)
    except requests.exceptions.ReadTimeout:
        time.sleep(5)  # Wait for 5 seconds before retrying
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(5)
