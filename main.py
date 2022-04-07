#!/usr/env/python3
#
# http://t.me/
#
#


from telegram.ext import *
import Constants as keys
import Responses as R


def cmd_start(update, context):
    update.message.reply_text('lets go')


def cmd_help(update, context):
    update.message.reply_text("I don't have all the answers.")


def cmd_upscale(update, context):
    update.message.reply_text("+1 UP")


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    update.message.reply_text(response)


def handle_error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", cmd_start))
    dp.add_handler(CommandHandler("help", cmd_help))
    dp.add_handler(CommandHandler("upscale", cmd_upscale))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(handle_error)

    updater.start_polling(5)
    updater.idle()



if __name__ == '__main__':
    main()