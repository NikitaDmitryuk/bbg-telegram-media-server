import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import os
import libtorrent as lt
import time
import sys
import shutil

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send me the torrent file and password in one message!")

async def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = update.message.caption
    if password == PASSWORD:
        file = await context.bot.get_file(update.message.document)
        fullfile = os.path.join(PATH_TO_SAVE_TORRENT_FILE, file.file_id)
        await file.download_to_drive(fullfile)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Authorisation Done. Wait for the download of the torrent file to complete.")
        info = lt.torrent_info(fullfile)
        h = ses.add_torrent({'ti': info, 'save_path': PATH_TO_SAVE_TORRENT_FILE})
        s = h.status()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="starting " + s.name)
        print('starting', s.name)
        i = 1
        current_time = 0
        time_step = 10

        while (not s.is_seeding):
            s = h.status()
            if i == 1 and current_time == 600:
                await remove(fullfile)
                await remove(os.path.join(PATH_TO_SAVE_TORRENT_FILE, h.status().name))
                break

            print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
                s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                s.num_peers, s.state), end=' ')

            if round(s.progress * 100) // 10 >= i:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='%s: %.2f%% complete (down: %.1f MB/s up: %.1f kB/s peers: %d)' % (h.status().name, s.progress * 100, s.download_rate / 1048576, s.upload_rate / 1024, s.num_peers))
                i += 1

            alerts = ses.pop_alerts()
            for a in alerts:
                if a.category() & lt.alert.category_t.error_notification:
                    print(a)

            time.sleep(time_step)
            current_time += time_step

        if not s.is_seeding:
            print(h.status().name, 'failed')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="An error has occurred!")
        else:
            print(h.status().name, 'complete')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="The movie \"{}\" is ready to watch!".format(h.status().name))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Authorisation Error!")

if __name__ == '__main__':
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

    PATH_TO_SAVE_TORRENT_FILE = './torrents'

    with open('./telegram-tokens/bbg-media-server-bot/Authorization_password.pwd', 'r') as file:
        PASSWORD = file.readline().replace('\n', '')

    with open('./telegram-tokens/bbg-media-server-bot/bot.token', 'r') as file:
        TOKEN = file.readline().replace('\n', '')

    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.Document.ALL, downloader))
    
    application.run_polling()
