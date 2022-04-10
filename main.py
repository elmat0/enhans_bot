#!/usr/env/python3
#
# enhance-bot
#
# Telegram bot to upscale images
#

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					 level=logging.INFO)

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, User, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, InlineQueryHandler
import Constants as keys
import Responses as R
import Database as db
import Commands as cmd


def main():
	updater = Updater(keys.API_KEY, use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler(["start","starten"], cmd.cmd_start))
	dp.add_handler(CommandHandler(["help","hilfen"], cmd.cmd_help))
	dp.add_handler(CommandHandler(["settings","einstellungen"], cmd.cmd_settings))
	dp.add_handler(CommandHandler(["upscale","skalieren"], cmd.cmd_upscale))	
	dp.add_handler(CommandHandler(["language","sprache"], cmd.cmd_set_language))
#	dp.add_handler(InlineQueryHandler(cmd_inline_caps))

	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_handler(CallbackQueryHandler(button))


	dp.add_error_handler(handle_error)

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()