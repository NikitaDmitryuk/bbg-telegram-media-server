import os
import shutil
import time
import math

import libtorrent as lt
from telegram import Update
from telegram.ext import ContextTypes

import bbg_telegram_media_server.config as config
import bbg_telegram_media_server.db_utils as db_utils


def delete(path: str) -> None:
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError("Path {} is not a file or dir.".format(path))


def download_torrent(file_id: str):
    full_file = os.path.join(config.PATH_TO_SAVE_TORRENT_FILE, file_id)
    info = lt.torrent_info(full_file)
    session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    handle = session.add_torrent({'ti': info, 'save_path': config.PATH_TO_SAVE_TORRENT_FILE})
    status = handle.status()
    print('starting', status.name)
    db_utils.add_movie(status.name, status.name, file_id)
    i = 1
    current_time = 0
    time_step = 10
    time_out = 600

    while not status.is_seeding:

        if i == 1 and current_time >= time_out:
            delete(full_file)
            delete(os.path.join(config.PATH_TO_SAVE_TORRENT_FILE, status.name))
            db_utils.remove_movie(status.name)
            session.remove_torrent(handle)
            break

        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
            status.progress * 100, status.download_rate / 1000, status.upload_rate / 1000,
            status.num_peers, status.state))

        if round(status.progress * 100) // 10 >= i:
            print("\"{}\": {}%".format(status.name, status.progress * 100))
            db_utils.update_downloaded_percentage(status.name, math.floor(status.progress * 100))
            i += 1

        alerts = session.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)

        time.sleep(time_step)
        current_time += time_step
        status = handle.status()

    if status.is_seeding:
        print(status.name, 'complete')
        db_utils.set_loaded(status.name)
    else:
        print(status.name, 'failed')


async def print_movie_list(movie_list, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for movie in movie_list:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ID: {}\nNAME: {}\nSTATUS: {}\n"
                                       .format(movie[0], movie[1],
                                               "downloaded" if movie[2] == 1 else
                                               "uploading - {}%".format(movie[3])))
