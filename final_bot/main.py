import telebot
import time
import datetime

from google_db import append
from user import User
from recovery import start_rec
from private.data import token, chat_id, true_token
from script import text_intro, text_group, text_after_sub,\
    text_succ_subs, text_name, text_surname, text_succ_register,\
    text_err_takt_subs, text_err_total, text_invalid_token,\
    text_already_reg, text_err

# user dict and class user to store name and surname
user_dict, token_set = start_rec()
temp_set = set()

# starting bot
bot = telebot.TeleBot(token)

# valid message if:
# 1. length is 2
# 2. second arg is numeric
# 3. token is unique (not it token set)
# 4. token is true, true in true_token()
# example "/start 098980809"
def is_valid_message(message):
    text = message.text.split(" ")
    if (len(text) == 2) and (text[1].isnumeric() == True) and\
        (text[1] not in token_set) and (true_token(text[1]) == True):
        return True
    return False


# extracts token from message
# DELETE this func later
def get_token(message):
    return message.text.split(" ")[1]


# reject in two cases:
# 1. user is NOT in DB, and WRONG TOKEN
# 2. user in DB. and SUCCESS
def rejector(message):
    val_token = is_valid_message(message)
    u_id = str(message.from_user.id)
    print(datetime.datetime.now(), message.from_user.id, ", TOKEN: ", val_token)
    if (u_id not in user_dict) and (val_token == False):
        return 1 # user not in db and token is invalid
    if (u_id in user_dict) and (user_dict[u_id].success == True):
        return 2 # you are already registered
    return 0


# init commands: start, help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(datetime.datetime.now(), message.from_user.id, ", MSG: ", message.text)
    start_num = rejector(message)
    if start_num == 0:
        u_id = str(message.from_user.id)
        if u_id not in user_dict:
            # adding user to local_db
            user_dict[u_id] = User()
            tkn = get_token(message)
            user_dict[u_id].token = tkn
            token_set.add(tkn)
        # authenticate
        bot.send_message(message.from_user.id, text_intro)
        bot.send_message(message.from_user.id, text_group)
        bot.send_message(message.from_user.id, text_after_sub)
    if start_num == 1:
        bot.send_message(message.from_user.id, text_invalid_token)
    if start_num == 2:
        bot.send_message(message.from_user.id, text_already_reg)


# step, where after success subscribe name is asked. Error otherwise
# A button instead could be added
@bot.message_handler(commands=['checkifsubs'])
def checkifsubs(message):
    print(datetime.datetime.now(), message.from_user.id, ", CHECKIFS")
    if (str(message.from_user.id) not in user_dict) or (rejector(message) != 0) or\
        (str(message.from_user.id) in temp_set):
        bot.send_message(message.from_user.id, text_err)
        return
    subscriber_bool = is_subs(message)
    if subscriber_bool:
        bot.send_message(message.from_user.id, text_succ_subs)
        name = bot.send_message(message.from_user.id, text_name)
        bot.register_next_step_handler(name, process_name_step)
    else:
        bot.send_message(message.from_user.id, text_err_takt_subs)


# function that checks if user is subscribed to group
def is_subs(message):
    try:
        res = bot.get_chat_member(chat_id, message.from_user.id)
        if (res.status == "left"):
            raise Exception()
        return True
    except Exception as ex:
        return False


# function that adds name and surname to db
def append_db(message):
    chat_id = str(message.from_user.id)
    user = user_dict[chat_id]
    append([[user.name, user.surname, str(datetime.datetime.now()), str(chat_id), str(user.token)]])


# saving name of user and asking for surname
def process_name_step(message):
    try:
        name = message.text
        assert type(name) == str and name.isalpha() == True
        user_dict[str(message.from_user.id)].name = name
        msg = bot.send_message(message.from_user.id, text_surname)
        bot.register_next_step_handler(msg, process_surname_step)
    except Exception as e:
        bot.reply_to(message, text_err_total)


# saving surname, appending creds to db, saying SUCCESS
def process_surname_step(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        # print("Surname text: ", surname, type(surname))
        assert type(surname) == str and surname.isalpha() == True
        user = user_dict[str(message.from_user.id)]
        user.surname = surname
        # print("before_db")
        temp_set.add(str(message.from_user.id))
        append_db(message)
        temp_set.remove(str(message.from_user.id))
        # print("after_db")
        user.success = True
        # insert_rec(user, message.chat.id)
        bot.send_message(chat_id, text_succ_register.format(user.name))
    except Exception as e:
        bot.reply_to(message, text_err_total)


# don't stop bot
# bot.polling(none_stop=True)
# bot.infinity_polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)  # или просто print(e) если у вас логгера нет,
        time.sleep(15)
