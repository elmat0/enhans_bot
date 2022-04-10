#!/usr/env/python3
#
# enhance-bot
#
# Telegram bot to upscale images
#

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					 level=logging.INFO)

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
import Constants as keys
import Responses as R

language = 'EN'


def get_response_text(update, context, msg):
	if msg in R.cmd_msgs:
		return str(R.cmd_msgs[msg][language])
	else:
		logging.error(f"msg not found - {msg}")

def send_response(update, context, msg):
	text = get_response_text(update, context, msg)
	if text:
		context.bot.send_message(
			chat_id=update.effective_chat.id
			,text=text
			,parse_mode = "HTML"
		)


def cmd_start(update, context):
	send_response(update,context,"start")


def cmd_help(update, context):
	send_response(update,context,"help")


def handle_text(update, context):
	text = str(update.message.text).lower()
	response = R.sample_responses(text)
	update.message.reply_text(response)


def handle_photo(update, context):
	send_response(update,context,"upscale_start")
	print("upscale function goes here")
	send_response(update,context,"upscale_end")
	error = True
	if error:
		send_response(update,context,"upscale_error")


def handle_error(update, context):
	print(f"\nUpdate {update} \n Caused error {context.error}\n")


def main():
	updater = Updater(keys.API_KEY, use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler(["start"], cmd_start))
	dp.add_handler(CommandHandler(["help"], cmd_help))
	dp.add_handler(MessageHandler(Filters.text, handle_text))
	dp.add_handler(MessageHandler(Filters.photo, handle_photo))

	dp.add_error_handler(handle_error)

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()