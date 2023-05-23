import Constants as keys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
import re

# Function to handle /start command
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a text with URLs to extract the first one.")

# Function to handle text messages
def handle_text(update: Update, context):
    text = update.message.text
    url = extract_url(text)
    if url:
        # Do something with the extracted URL
        context.bot.send_message(chat_id=update.effective_chat.id, text="Extracted URL: " + url)
    else:
        # No URL found
        context.bot.send_message(chat_id=update.effective_chat.id, text="No URL found")

# Function to extract the first HTTP URL from text
def extract_url(text):
    url_regex = r"(https?://\S+)"
    match = re.search(url_regex, text)
    if match:
        return match.group(1)
    else:
        return None

# Set up the Telegram bot
def main():
    # Initialize the bot
    updater = Updater(keys.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Register message handler
    text_handler = MessageHandler(Filters.text, handle_text)
    dispatcher.add_handler(text_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()