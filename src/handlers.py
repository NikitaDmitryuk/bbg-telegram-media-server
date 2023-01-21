import os

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters, MessageHandler
import asyncio

from utils import download_torrent
import global_variable
import sqlite_utils
import utils

AUTHORIZATION_FAILED_MESSAGE = "Authorisation failed. Use /login <password>."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send me the torrent file and password in one message!")

async def get_movie_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if sqlite_utils.check_user(update.effective_chat.id):
        movie_list = sqlite_utils.get_movie_list()
        if len(movie_list) > 0:
            await utils.print_movie_list(movie_list, update, context)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Movie list is empty!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=AUTHORIZATION_FAILED_MESSAGE)

async def authorization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    auth_status = False
    password = update.message.text.replace('/login', '').replace(' ', '')
    if password is not None:
        auth_status = sqlite_utils.login(password, update.effective_chat.id, update.effective_chat.full_name)

    if auth_status:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Authorisation Done.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=AUTHORIZATION_FAILED_MESSAGE)

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if sqlite_utils.check_user(update.effective_chat.id):
        file = await context.bot.get_file(update.message.document)
        full_file = os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, file.file_id)
        await file.download_to_drive(full_file)

        torrent_task = asyncio.create_task(download_torrent(update, context, file.file_id))
        await torrent_task
        torrent_status = torrent_task.result()

        if torrent_status.is_seeding:
            print(torrent_status.name, 'complete')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="The movie \"{}\" is ready to watch!".format(torrent_status.name))
            sqlite_utils.set_loaded(torrent_status.name)
        else:
            print(torrent_status.name, 'failed')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="\"{}\": An error has occurred!".format(torrent_status.name))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=AUTHORIZATION_FAILED_MESSAGE)

start_handler = CommandHandler('start', start)
get_movie_list_handler = CommandHandler('getlist', get_movie_list)
login_handler = CommandHandler('login', authorization)
download_handler = MessageHandler(filters.Document.ALL, download_file)
application_handlers = [start_handler, get_movie_list_handler, login_handler, download_handler]
