import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time
import requests
import json

API_TOKEN = '7367410479:AAG2lm0_YWlbtry9enSf2Z7Bpd7maqSdXtg'  # Замените на ваш токен

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения ID последних отправленных сообщений для каждого чата
last_message_ids = {}
# Словарь для хранения ID последнего сообщения пользователя для каждого чата
last_user_message_id = {}

# Загрузка опций из JSON файла
with open('options.json', 'r', encoding='utf-8') as file:
    options = json.load(file)

# Функция для удаления последних сообщений, отправленных ботом
def delete_last_messages(chat_id):
    if chat_id in last_message_ids:
        for message_id in last_message_ids[chat_id]:
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение бота: {e}")
        last_message_ids[chat_id] = []

# Функция для удаления последнего сообщения пользователя
def delete_last_user_message(chat_id):
    if chat_id in last_user_message_id:
        try:
            bot.delete_message(chat_id, last_user_message_id[chat_id])
        except Exception as e:
            print(f"Не удалось удалить сообщение пользователя: {e}")

# Функция для отправки фото и текста с кнопкой "Вернуться к выбору"
def send_option_photo_with_button(chat_id, photo_url, caption):
    # Создаем клавиатуру с кнопкой "Вернуться к выбору"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back_button = KeyboardButton('Вернуться к выбору')
    markup.add(back_button)
    
    # Отправляем фото с подписью и клавиатурой
    sent_message = bot.send_photo(chat_id, photo_url, caption, reply_markup=markup)
    return sent_message

# Функция для отправки приветственного сообщения с клавиатурой
def send_option_menu(chat_id):
    # Создаем клавиатуру с кнопками
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in options.keys():
        markup.add(KeyboardButton(option))
    
    # Отправляем новое сообщение и сохраняем его ID
    sent_message = bot.send_message(chat_id, "Добро пожаловать! Пожалуйста, выберите одну из опций:", reply_markup=markup)
    if chat_id not in last_message_ids:
        last_message_ids[chat_id] = []
    last_message_ids[chat_id].append(sent_message.message_id)

# Функция для отправки меню с командами
def send_command_menu(chat_id):
    command_list = "/start - Начать заново\n/menu - Показать это меню\n/set_avatar - Установить аватарку\n"
    sent_message = bot.send_message(chat_id, f"Доступные команды:\n{command_list}")
    if chat_id not in last_message_ids:
        last_message_ids[chat_id] = []
    last_message_ids[chat_id].append(sent_message.message_id)

# Функция для установки аватарки бота
def set_bot_profile_photo(photo_path):
    url = f"https://api.telegram.org/bot{API_TOKEN}/setChatPhoto"
    with open(photo_path, 'rb') as photo:
        files = {'photo': photo}
        response = requests.post(url, files=files)
        return response.json()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Удаляем предыдущие сообщения бота и пользователя
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    # Сохраняем ID последнего сообщения пользователя
    last_user_message_id[message.chat.id] = message.message_id
    
    # Отправляем меню с вариантами выбора
    send_option_menu(message.chat.id)

# Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def send_menu(message):
    # Удаляем предыдущие сообщения бота и пользователя
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    # Сохраняем ID последнего сообщения пользователя
    last_user_message_id[message.chat.id] = message.message_id
    
    # Отправляем меню команд
    send_command_menu(message.chat.id)

# Обработчик команды /set_avatar
@bot.message_handler(commands=['set_avatar'])
def handle_set_avatar(message):
    # Путь к фото
    photo_path = 'path_to_your_photo.jpg'  # Замените на путь к вашему фото
    result = set_bot_profile_photo(photo_path)
    
    # Отправляем результат выполнения команды
    bot.send_message(message.chat.id, f"Результат установки аватарки: {result}")

# Обработчик нажатий кнопок
@bot.message_handler(func=lambda message: message.text in options.keys())
def handle_option(message):
    # Удаляем предыдущие сообщения бота и пользователя
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    # Сохраняем ID последнего сообщения пользователя
    last_user_message_id[message.chat.id] = message.message_id
    
    option = options[message.text]
    photo_url = option['photo_url']
    caption = option['caption']
    
    sent_photo_message = send_option_photo_with_button(message.chat.id, photo_url, caption)
    if message.chat.id not in last_message_ids:
        last_message_ids[message.chat.id] = []
    last_message_ids[message.chat.id].append(sent_photo_message.message_id)

# Обработчик кнопки "Вернуться к выбору"
@bot.message_handler(func=lambda message: message.text == 'Вернуться к выбору')
def handle_back_to_menu(message):
    # Удаляем предыдущие сообщения бота и пользователя
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    # Сохраняем ID последнего сообщения пользователя
    last_user_message_id[message.chat.id] = message.message_id
    
    # Отправляем меню с вариантами выбора
    send_option_menu(message.chat.id)

# Обработчик нажатия кнопки "Меню"
@bot.message_handler(func=lambda message: message.text == 'Меню')
def handle_menu_button(message):
    # Отправляем inline-клавиатуру с командами
    markup = InlineKeyboardMarkup()
    markup.row_width = 1  # Отображаем кнопки в один столбец
    
    command_list = "/start - Начать заново\n/menu - Показать это меню\n"
    command_buttons = [
        InlineKeyboardButton("Показать команды", callback_data='show_commands'),
    ]
    markup.add(*command_buttons)
    
    bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)

# Обработчик inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == 'show_commands':
        send_command_menu(call.message.chat.id)

# Запуск бота с увеличенным таймаутом и механизмом повторных попыток
while True:
    try:
        bot.polling(timeout=60, long_polling_timeout=60)
    except requests.exceptions.ReadTimeout:
        time.sleep(5)  # Ожидание 5 секунд перед повторной попыткой
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        time.sleep(5)
