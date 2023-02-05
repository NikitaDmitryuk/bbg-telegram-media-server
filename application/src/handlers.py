#!python
#cython: language_level=3

import os
import threading

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters, MessageHandler

from utils import download_torrent
import config
import db_utils
import utils

AUTHORIZATION_FAILED_MESSAGE = "Authorisation failed. Use /login <password>."
START_MESSAGE = "Send me:\n/login <password> - for registration\n<torrent_file> - to download a file\n/getlist - to " \
                "get a list of files\n/rm <file_id> - to delete a file"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE)


async def remove_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HINT = "Use /getlist to get file id, then /rm <file_id>"
    if db_utils.check_user(update.effective_chat.id):
        movie_id = update.message.text.replace('/rm', '').replace(' ', '')
        if not movie_id.isnumeric():
            return await context.bot.send_message(chat_id=update.effective_chat.id, text=HINT)

        movie_files = db_utils.get_movie_by_id(movie_id)
        if movie_files:
            movie_file = os.path.join(config.PATH_TO_SAVE_TORRENT_FILE, movie_files[1])
            torrent_file = os.path.join(config.PATH_TO_SAVE_TORRENT_FILE, movie_files[2])
            utils.delete(movie_file)
            utils.delete(torrent_file)
            db_utils.remove_movie(movie_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Movie \"{movie_files[0]}\" deleted!")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=HINT)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=AUTHORIZATION_FAILED_MESSAGE)


async def get_movie_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if db_utils.check_user(update.effective_chat.id):
        movie_list = db_utils.get_movie_list()
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
        auth_status = db_utils.login(password, update.effective_chat.id, update.effective_chat.full_name)

    if auth_status:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Authorisation Done.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=AUTHORIZATION_FAILED_MESSAGE)


async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if db_utils.check_user(update.effective_chat.id):
        file = await context.bot.get_file(update.message.document)
        full_file = os.path.join(config.PATH_TO_SAVE_TORRENT_FILE, file.file_id)
        await file.download_to_drive(full_file)

        thread = threading.Thread(target=download_torrent, args=(file.file_id,))
        thread.start()

        context.bot.send_message(chat_id=update.effective_chat.id, text="Download started!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=AUTHORIZATION_FAILED_MESSAGE)


start_handler = CommandHandler('start', start)
remove_handler = CommandHandler('rm', remove_movie)
get_movie_list_handler = CommandHandler('getlist', get_movie_list)
login_handler = CommandHandler('login', authorization)
download_handler = MessageHandler(filters.Document.ALL, download_file)
application_handlers = [start_handler, remove_handler, get_movie_list_handler, login_handler, download_handler]
