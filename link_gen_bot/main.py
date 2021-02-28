import telebot
import datetime
import time

from google_db import get_value
from private.data import token, bot_name, list_id, gen_token

bot = telebot.TeleBot(token)

is_busy_set = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("\n", datetime.datetime.now(), "Hello user ", message.from_user.id)
    if message.from_user.id not in list_id:
        # print(message.from_user.id)
        bot.send_message(message.from_user.id, 'ERROR')    
        return
    if len(is_busy_set) != 0:
        print(is_busy_set)
        bot.send_message(message.from_user.id, 'ERROR, BUSY')    
        return
    is_busy_set.add(message.from_user.id)
    bot.send_message(message.from_user.id, 'Link is generating...')
    print(datetime.datetime.now(), "Before req ", message.from_user.id)
    token = get_value()
    print(datetime.datetime.now(), "After req ", message.from_user.id)
    token = gen_token(token)
    link = f"https://t.me/{bot_name}?start={token}"
    bot.send_message(message.from_user.id, link)
    is_busy_set.clear()


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        is_busy_set.clear()
        time.sleep(15)
