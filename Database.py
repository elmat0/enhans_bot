#!/usr/env/python3
#
# enhance-bot
#
# Telegram bot to upscale images
#

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data

import logging
from telegram import User 
from telegram.ext import Updater, CommandHandler


def show_db(update, context):
    print(context.user_data)


def set_value(update, context, key, value):
    try:
        context.user_data[key] = value
        logging.info(f"{update.effective_chat.id} -  Set '{key}' to '{value}'")
    except KeyError:
        logging.error(f"key not found - {key}")


def get_value(update, context, key):
    try:
        value = context.user_data.get(key, 'Not found')
        return value
    except KeyError:
        logging.error(f"key not found - {key}")



def setup_db(update, context):
    language_code = str(User.language_code).upper()
    if language_code in ["EN", "DE"]:
        set_value(update, context, "language", language_code)
    else:
        set_value(update, context, "language", "EN")

    set_value(update, context, "scale", 2)
    
