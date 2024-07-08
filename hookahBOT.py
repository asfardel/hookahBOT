import os
import telebot
import requests
import json

API_TOKEN = '7367410479:AAG2lm0_YWlbtry9enSf2Z7Bpd7maqSdXtg'  

bot = telebot.TeleBot(API_TOKEN)


last_message_ids = {}
last_user_message_id = {}

with open('options.json', 'r', encoding='utf-8') as file:
    options = json.load(file)

def delete_last_messages(chat_id):
    if chat_id in last_message_ids:
        for message_id in last_message_ids[chat_id]:
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение бота: {e}")
        last_message_ids[chat_id] = []

def delete_last_user_message(chat_id):
    if chat_id in last_user_message_id:
        try:
            bot.delete_message(chat_id, last_user_message_id[chat_id])
        except Exception as e:
            print(f"Не удалось удалить сообщение пользователя: {e}")

def send_option_photo_with_button(chat_id, photo_url, caption):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back_button = telebot.types.KeyboardButton('Вернуться к выбору')
    markup.add(back_button)
    
    sent_message = bot.send_photo(chat_id, photo_url, caption, reply_markup=markup)
    return sent_message

def send_option_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in options.keys():
        markup.add(telebot.types.KeyboardButton(option))
    
    sent_message = bot.send_message(chat_id, "Добро пожаловать! Пожалуйста, выберите одну из опций:", reply_markup=markup)
    if chat_id not in last_message_ids:
        last_message_ids[chat_id] = []
    last_message_ids[chat_id].append(sent_message.message_id)

def send_command_menu(chat_id):
    command_list = "/start - Начать заново\n/menu - Показать это меню\n/set_avatar - Установить аватарку\n"
    sent_message = bot.send_message(chat_id, f"Доступные команды:\n{command_list}")
    if chat_id not in last_message_ids:
        last_message_ids[chat_id] = []
    last_message_ids[chat_id].append(sent_message.message_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    last_user_message_id[message.chat.id] = message.message_id

    send_option_menu(message.chat.id)


@bot.message_handler(commands=['menu'])
def send_menu(message):
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    last_user_message_id[message.chat.id] = message.message_id
    
    send_command_menu(message.chat.id)

@bot.message_handler(commands=['set_avatar'])
def handle_set_avatar(message):
    photo_path = 'path_to_your_photo.jpg'
    result = set_bot_profile_photo(photo_path)
    
    bot.send_message(message.chat.id, f"Результат установки аватарки: {result}")

@bot.message_handler(func=lambda message: message.text in options.keys())
def handle_option(message):
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    last_user_message_id[message.chat.id] = message.message_id
    
    option = options[message.text]
    photo_url = option['photo_url']
    caption = option['caption']
    
    sent_photo_message = send_option_photo_with_button(message.chat.id, photo_url, caption)
    if message.chat.id not in last_message_ids:
        last_message_ids[message.chat.id] = []
    last_message_ids[message.chat.id].append(sent_photo_message.message_id)

@bot.message_handler(func=lambda message: message.text == 'Вернуться к выбору')
def handle_back_to_menu(message):
    delete_last_messages(message.chat.id)
    delete_last_user_message(message.chat.id)
    
    last_user_message_id[message.chat.id] = message.message_id
    
    send_option_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == 'Меню')
def handle_menu_button(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1 
    
    command_list = "/start - Начать заново\n/menu - Показать это меню\n"
    command_buttons = [
        telebot.types.InlineKeyboardButton("Показать команды", callback_data='show_commands'),
    ]
    markup.add(*command_buttons)
    
    bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == 'show_commands':
        send_command_menu(call.message.chat.id)

while True:
    try:
        bot.polling(timeout=60, long_polling_timeout=60)
    except requests.exceptions.ReadTimeout:
        time.sleep(5) 
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        time.sleep(5)