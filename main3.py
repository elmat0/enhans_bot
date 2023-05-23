#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Botlife Enhancements
"""
import Constants as keys
import logging
from html import escape
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode, ChatAction
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

from transformers.tools.base import Tool, get_default_device
from transformers.utils import is_accelerate_available

from diffusers import DiffusionPipeline

from telegram.ext import filters, MessageHandler, Application, CommandHandler, ContextTypes, InlineQueryHandler
import sqlite3
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from math import floor
import textwrap
import logging
from functools import wraps
logging.getLogger("transformers").setLevel(logging.ERROR)

VERSION = "v0.0.5"
CORPUS_DB = "corpus.db"

# MODELS
SUMMARY_MODEL = "knkarthick/MEETING_SUMMARY"
SUMMARY_MIN_LENGTH = 16
SUMMARY_MAX_LENGTH = 1024
CAPTION_MODELS = {
    'blip-base': 'Salesforce/blip-image-captioning-base',
    'blip-large': 'Salesforce/blip-image-captioning-large',
    'blip2-2.7b': 'Salesforce/blip2-opt-2.7b',
    'blip2-flan-t5-xl': 'Salesforce/blip2-flan-t5-xl',
    'vit-gpt2-coco-en':'ydshieh/vit-gpt2-coco-en',
}
CAPTION_MODEL = CAPTION_MODELS['blip-base']
CAPTION_DEVICE = "cpu"
QUESTION_MODEL = "deepset/roberta-base-squad2"
QUERY_IMAGE_MODEL = "impira/layoutlm-document-qa"
TXT2VID_MODEL="damo-vilab/text-to-video-ms-1.7b"

# GO ----------------------------------------------------------------------------------
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
conn = sqlite3.connect(CORPUS_DB)
conn.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        article_title TEXT,
        article_text TEXT,
        summary_short TEXT,
        summary_long TEXT
    )
""")

# Utils

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    return decorator

# Define a few command handlers. These usually take the two arguments update and
# context.

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    message = f"""<b>Salute!</b>🍻 

<pre>Send me an image and I'll tell you what I see.</pre>

Or try these commands:

<b>/start, /help</b>
<pre>This.</pre>

<b>/summary, /s [url]</b>
<pre>Summarise a website.</pre>

<b>/question, /q [some text]</b>
<pre>Ask me a question.</pre>

<i>{VERSION}</i>
"""
    await update.message.reply_html(textwrap.dedent(message))


@send_action(ChatAction.UPLOAD_PHOTO)
async def caption_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = "unknown"
    image_file = await update.message.photo[-1].get_file()
    print(image_file)
    captioner = pipeline("image-to-text", model=CAPTION_MODEL, max_new_tokens=50, device=CAPTION_DEVICE, use_fast=True)
    caption = captioner(image_file.file_path)
    if caption[0]['generated_text']:
        answer = caption[0]['generated_text']
    await update.message.reply_text(answer)


@send_action(ChatAction.TYPING)
async def query_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """What is happening in this pic?"""
    print(context.args)
    answer = "Give me an image and a question."
    question = " ".join(context.args)
    question = f"{question}?"
    if question != "?":
        nlp = pipeline(
            "document-question-answering",
            model=QUERY_IMAGE_MODEL
        )
        print (nlp)
        answer = nlp(
            #TODO pass in real image
            "https://i.redd.it/k2qcdisoy71b1.jpg",
            question
        )
        print(answer)
    await update.message.reply_text(answer)

@send_action(ChatAction.TYPING)
async def question_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """What have we learnt?"""
    qa_model = pipeline("question-answering",QUESTION_MODEL)
    question = " ".join(context.args)
    question = f"{question}?"
    answer = "Ask me a question."
    if question != "?":
        cursor = conn.execute('SELECT summary_long FROM links')
        knowledge = "".join([y for x in cursor.fetchall() for y in x])
        answer = qa_model(question = question, context = knowledge)["answer"]
    await update.message.reply_text(answer)

async def corpus_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide insights into bots knowledge / bias"""
    cursor = conn.execute('SELECT id, article_title FROM links')
    corpus = cursor.fetchall()
    await update.message.reply_text(f"{corpus}")

@send_action(ChatAction.TYPING)
async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarise a website via URL"""


    def scrape_web_article(url):
        try:
            response = requests.get(url)
        except requests.exceptions.MissingSchema as e:
            response = requests.get(f"https://{url}")
        
        soup = BeautifulSoup(response.content, "html.parser")
        article_title = " ".join([e.get_text() for e in soup.find_all("title")])
        article_text = " ".join([e.get_text() for e in soup.find_all("p")])
        return {"title":article_title, "text":article_text}

    def generate_summary(raw_text):
        text_length = len(raw_text)
        return generator(
                raw_text
                ,min_length = SUMMARY_MIN_LENGTH
                ,max_length = SUMMARY_MAX_LENGTH
                ,truncation=True
            )[0]["summary_text"]

    url = " ".join(context.args)
    answer = "Give me a URL"
    if url != "":
        generator = pipeline("summarization", model=SUMMARY_MODEL)
        scrape = scrape_web_article(url)
        summary_short = 'NA'
        summary_long = 'NA'
        if len(scrape["title"]) > 0:
            summary_short = generate_summary(scrape["title"])
        if len(scrape["text"]) > 0:
            summary_long = generate_summary(scrape["text"])
        #TODO prevent dups
        #cursor = conn.execute("SELECT url from links where url like '?'",(url))
        #if cursor.fetchall()[0] != url:
        #print('new info')
        conn.execute('INSERT INTO links (url, article_title, article_text, summary_short, summary_long) VALUES (?, ?, ?, ?, ?)', 
                    (url, scrape["title"], scrape["text"], summary_short, summary_long))
        conn.commit()
        answer = summary_long
        #else: 
        #    print('old info')
    await update.message.reply_text(textwrap.dedent(answer))


@send_action(ChatAction.UPLOAD_VIDEO)
async def txt2vid_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # generator = pipeline("summarization", model='damo-vilab/modelscope-damo-text-to-video-synthesis')

    # test_text = {
    #         'text': 'A panda eating bamboo on a rock.',
    #     }
    # output_video_path = generator(test_text,)[OutputKeys.OUTPUT_VIDEO]
    # print('output_video_path:', output_video_path)

    
    # pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
    # pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    # pipe.enable_model_cpu_offload()

    # prompt = "Spiderman is surfing"
    # video_frames = pipe(prompt, num_inference_steps=25).frames
    # video_path = export_to_video(video_frames)
    # print(video_path)

    await update.message.reply_video(video)










def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(keys.API_KEY).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", start_command))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("s", summary_command))
    application.add_handler(CommandHandler("question", question_command))
    application.add_handler(CommandHandler("q", question_command))
    application.add_handler(CommandHandler("query_image", question_command))
    application.add_handler(CommandHandler("qi", query_image_command))
    application.add_handler(CommandHandler("t2v", txt2vid_command))
    application.add_handler(CommandHandler("caption_image", caption_image_command))
    application.add_handler(CommandHandler("ci", caption_image_command))

    # handle specific message types
    application.add_handler(MessageHandler(filters.PHOTO, caption_image_command))
    application.add_handler(MessageHandler(filters.PHOTO & filters.TEXT, query_image_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, question_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()