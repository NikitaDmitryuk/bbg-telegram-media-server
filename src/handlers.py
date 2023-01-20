import os

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters, MessageHandler

from utils import download_torrent
import global_variable
import sqlite_utils


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send me the torrent file and password in one message!")

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.caption
    if password == global_variable.PASSWORD:
        file = await context.bot.get_file(update.message.document)
        full_file = os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, file.file_id)
        await file.download_to_drive(full_file)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Authorisation Done. Wait for the download of the torrent file to complete.")

        torrent_status = await download_torrent(update, context, file.file_id)

        if torrent_status.is_seeding:
            print(torrent_status.name, 'complete')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="The movie \"{}\" is ready to watch!".format(torrent_status.name))
            sqlite_utils.set_loaded(torrent_status.name)
        else:
            print(torrent_status.name, 'failed')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="\"{}\": An error has occurred!".format(torrent_status.name))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Authorisation Error!")

start_handler = CommandHandler('start', start)
download_handler = MessageHandler(filters.Document.ALL, download_file)
application_handlers = [start_handler, download_handler]
