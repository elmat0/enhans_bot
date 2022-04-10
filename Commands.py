#!/usr/env/python3
#
# enhance-bot
#
# Telegram bot to upscale images
#



def get_msg(update, context, msg):
	language = db.get_value(update, context, 'language')
	if msg in R.cmd_msgs:
		return str(R.cmd_msgs[msg][language])
	else:
		logging.error(f"msg not found - {msg}")


def send_html(update, context, html):
	context.bot.send_message(
		chat_id=update.effective_chat.id
		,text=html
		,parse_mode = "HTML"
	)


def send_msg(update, context, msg):
	html = get_msg(update, context, msg)
	send_html(update, context, html)




def cmd_start(update, context):
	db.setup_db(update, context)
	send_msg(update,context,"start")
	
	

def cmd_help(update, context):
	send_msg(update,context,"help")


def cmd_settings(update, context):
	send_msg(update,context,"settings")


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


# def cmd_set_language(update, context):
# 	try:
# 		first_arg = context.args[0].upper()
# 		if first_arg in ['EN', 'DE']:
# 			db.set_value(update, context, 'language', first_arg)
# 	except:
# 		print('aiiieee')


def cmd_set_language(update, context):
	keyboard = InlineKeyboardMarkup([[
			InlineKeyboardButton("EN", callback_data='EN'),
			InlineKeyboardButton("DE", callback_data='DE')
		]])
	prompt_msg = "Select Language" #get_msg(update, context, "language_select")
	update.message.reply_text(prompt_msg, reply_markup=keyboard)


#	db.set_value(update, context, "language", language)




def button(update, context):
	query = update.callback_query
	print(query.message)
	query.answer()
	print(query.message)

	print(query.data)
	query.edit_message_text(text=f"Selected: {query.data}")
	


def handle_message(update, context):
	text = str(update.message.text).lower()
	response = R.sample_responses(text)
	update.message.reply_text(response)


def handle_error(update, context):
	logging.error(f"\nUpdate {update} \n Caused error {context.error}\n")
