#!/usr/env/python3
#
# enhans_bot
#
# Telegram bot to upscale images
#
# Main logic loop goes here

import os
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					 level=logging.INFO)

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto, File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
import Constants as keys
import Responses as R

language = 'EN'


def get_response_text(update, context, msg):
	if msg in R.cmd_msgs:
		return str(R.cmd_msgs[msg][language])
	else:
		logging.error(f"msg not found - {msg}")

def send_response(update, context, msg, mode="send", chat_id=None, message_id=None):

	text = get_response_text(update, context, msg)

	if text:
		if mode == "send":
			heh = context.bot.send_message(
				chat_id=update.effective_chat.id
				,text=text
				,parse_mode = "HTML"
			)
			chat_id = heh.chat['id']
			message_id = heh['message_id']
		if mode == "edit":
			context.bot.edit_message_text(
				chat_id=chat_id
				,message_id=message_id
				,text=text
				,parse_mode = "HTML"
			)
		return {"chat_id" : chat_id, "message_id" : message_id}

def cmd_start(update, context):
	send_response(update,context,"start")


def cmd_help(update, context):
	send_response(update,context,"help")


def handle_text(update, context):
	text = str(update.message.text).lower()
	response = R.sample_responses(text)
	update.message.reply_text(response)


def handle_photo(update, context):
	""" Handle and upscale an image
		TODO This needs proper job_queue implementation
	"""
	
	photos = update.message.photo
	
	if photos:
		# if we really have photos select largest
		file_unique_id = photos[-1]['file_unique_id']
		image_file = photos[-1].get_file()

		# setup some filepaths
		if not os.path.exists("img"):
			os.mkdir("img")
		src_file = f"img/{file_unique_id}.png"
		dst_file = f"img/{file_unique_id}_x2.png"


		# pin a single chat / message ID to use for status updates
		# then download image
		message_info = send_response(update,context,"upscale_download")
		chat_id = message_info['chat_id']
		message_id = message_info['message_id']

		image_file.download(custom_path=src_file)

		# upscale image
		send_response(update,context,"upscale_start", 
			mode="edit"	,chat_id=chat_id ,message_id=message_id)
		if os.path.isfile(src_file):
			# <MAGIC HAPPENS>
		 	os.system(f"convert {src_file} -resize 200% {dst_file}")
			# </MAGIC HAPPENS>

		# send image to chat and update status
		send_response(update,context,"upscale_upload", 
			mode="edit"	,chat_id=chat_id ,message_id=message_id)
		if os.path.isfile(dst_file):
			context.bot.send_document(chat_id=message_info['chat_id']
				, document=open(dst_file, 'rb'))
			send_response(update,context,"upscale_end", 
				mode="edit"	,chat_id=chat_id ,message_id=message_id)

	else:
		send_response(update,context,"upscale_error", mode="edit"
			,chat_id=message_info['chat_id']
			,message_id=message_info['message_id'])


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