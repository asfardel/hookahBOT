import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
import time
import requests

API_TOKEN = '7367410479:AAG2lm0_YWlbtry9enSf2Z7Bpd7maqSdXtg'

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения ID последнего отправленного сообщения для каждого чата
last_message_id = {}

# Функция для удаления последнего сообщения, отправленного ботом
def delete_last_message(chat_id):
    if chat_id in last_message_id:
        try:
            bot.delete_message(chat_id, last_message_id[chat_id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")

# Функция для отправки фото и текста
def send_option_photo(chat_id, photo_url, caption):
    sent_message = bot.send_photo(chat_id, photo_url, caption)
    return sent_message

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Удаляем предыдущее сообщение бота
    delete_last_message(message.chat.id)
    
    # Создаем клавиатуру с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = KeyboardButton('перечная мята')
    button2 = KeyboardButton('кислая вишня')
    button3 = KeyboardButton('гранат')
    markup.add(button1, button2, button3)
    
    # Отправляем новое сообщение и сохраняем его ID
    sent_message = bot.send_message(message.chat.id, "Добро пожаловать! Пожалуйста, выберите одну из опций:", reply_markup=markup)
    last_message_id[message.chat.id] = sent_message.message_id

# Обработчик нажатий кнопок
@bot.message_handler(func=lambda message: message.text in ['перечная мята', 'кислая вишня', 'гранат'])
def handle_option(message):
    # Удаляем предыдущее сообщение бота
    delete_last_message(message.chat.id)
    
    # Словарь с фото для каждой опции
    options = {
        'перечная мята': {
            'photo_url': 'photo/myata.jpg',
            'caption': "перечная мяты"
        },
        'кислая вишня': {
            'photo_url': 'photo/vishnya.jpg',
            'caption': "вишня"
        },
        'гранат': {
            'photo_url': 'photo/granat.jpg',
            'caption': "гранат"
        }
    }
    
    option = options[message.text]
    photo_url = option['photo_url']
    caption = option['caption']
    
    sent_message = send_option_photo(message.chat.id, photo_url, caption)
    
    # Сохраняем ID последнего сообщения
    last_message_id[message.chat.id] = sent_message.message_id

# Запуск бота с увеличенным таймаутом и механизмом повторных попыток
while True:
    try:
        bot.polling(timeout=60, long_polling_timeout=60)
    except requests.exceptions.ReadTimeout:
        time.sleep(5)  # Ожидание 5 секунд перед повторной попыткой
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        time.sleep(5)
