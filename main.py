#!/usr/env/python3
#
# http://t.me/
#
#

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
import Constants as keys
import Responses as R

language = 'EN'

def send_msg(update, context, msg):
    if msg in R.cmd_msgs:
        context.bot.send_message(
            chat_id=update.effective_chat.id
            ,text=R.cmd_msgs[msg][language]
            ,parse_mode = "HTML"
        )
    else:
        logging.error(f"msg not found - {msg}") 


def cmd_start(update, context):
    send_msg(update,context,"start")
    

def cmd_help(update, context):
    send_msg(update,context,"help")
   

def cmd_upscale(update, context):
    send_msg(update,context,"upscale_start")
    print("upscale function goes here")
    error = True
    if error:
        send_msg(update,context,"upscale_error")


def cmd_inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def cmd_set_language(update, context):
    pass


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    update.message.reply_text(response)


def handle_error(update, context):
    print(f"\nUpdate {update} \n Caused error {context.error}\n")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(["start","starten"], cmd_start))
    dp.add_handler(CommandHandler(["help","hilfen"], cmd_help))
    dp.add_handler(CommandHandler(["upscale","skalieren"], cmd_upscale))
    dp.add_handler(CommandHandler(["language","sprache"], cmd_set_language))
    dp.add_handler(InlineQueryHandler(cmd_inline_caps))


    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(handle_error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()