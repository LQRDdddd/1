import telebot
import datetime
import os
import schedule
import time
import threading


API_TOKEN = 'ihefihoew'
bot = telebot.TeleBot(API_TOKEN)

# Путь к файлам с сообщениями

current_dir = os.path.dirname(__file__)
daily_message_path = os.path.join(current_dir, 'daily_message.txt')
biweekly_message_path = os.path.join(current_dir, 'biweekly_message.txt')

# Словарь для хранения пользовательских сообщений

user_messages = {}

# Функция для отправки ежедневного сообщения

def send_daily_message():
    for group_id, message in user_messages.items():
        bot.send_message(group_id, message + " (Это ежедневное сообщение)")

# Функция для отправки сообщения раз в две недели
        
def send_biweekly_message():
    for group_id, message in user_messages.items():
        bot.send_message(group_id, message + " (Это сообщение раз в две недели)")

# Обработчик команды /setmessage
        
@bot.message_handler(commands=['setmessage'])
def set_message(message):
    chat_id = message.chat.id
    user_message = message.text.replace('/setmessage', '').strip()
    user_messages[chat_id] = user_message
    bot.send_message(chat_id, "Сообщение успешно установлено")

# Обработчик команды /deletemessage
    
@bot.message_handler(commands=['deletemessage'])
def delete_message(message):
    chat_id = message.chat.id
    if chat_id in user_messages:
        del user_messages[chat_id]
        bot.send_message(chat_id, "Сообщение успешно удалено")

# Расписание для ежедневных сообщений
        
schedule.every().day.at("09:00").do(send_daily_message)

# Расписание для сообщений раз в две недели (понедельник)

schedule.every().monday.at("10:00").do(send_biweekly_message)

# Функция для запуска планировщика

def schedule_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск планировщика в отдельном потоке
        
t = threading.Thread(target=schedule_jobs)
t.start()

# Функция для определения правильности команд и сообщений

def check_input(message):
    if len(message.text.split()) < 2:
        return False
    return True

# Обработчик входящих сообщений

@bot.message_handler(func=check_input)
def handle_message(message):
    bot.reply_to(message, "Неверная команда или сообщение. Пожалуйста, укажите корректное значение.")

# Запускаем бота
    
bot.polling()