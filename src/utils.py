import os
import shutil
import time
import math

import libtorrent as lt
from telegram import Update
from telegram.ext import ContextTypes

import global_variable
import sqlite_utils


def delete(path):
    """path could either be relative or absolute. """
    # check if file or directory exists
    if os.path.isfile(path) or os.path.islink(path):
        # remove file
        os.remove(path)
    elif os.path.isdir(path):
        # remove directory and all its content
        shutil.rmtree(path)
    else:
        raise ValueError("Path {} is not a file or dir.".format(path))


def download_torrent(file_id):
    full_file = os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, file_id)
    info = lt.torrent_info(full_file)
    session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    handle = session.add_torrent({'ti': info, 'save_path': global_variable.PATH_TO_SAVE_TORRENT_FILE})
    status = handle.status()
    print('starting', status.name)
    sqlite_utils.add_movie(status.name, status.name, file_id)
    i = 1
    current_time = 0
    time_step = 10
    time_out = 600

    while (not status.is_seeding):
        
        if i == 1 and current_time >= time_out:
            delete(full_file)
            delete(os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, status.name))
            sqlite_utils.remove_movie(status.name)
            session.remove_torrent(handle)
            break

        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
            status.progress * 100, status.download_rate / 1000, status.upload_rate / 1000,
            status.num_peers, status.state), end=' ')

        if round(status.progress * 100) // 10 >= i:
            print("\"{}\": {}%".format(status.name, status.progress * 100))
            sqlite_utils.update_downloaded_percentage(status.name, math.floor(status.progress * 100))
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
        sqlite_utils.set_loaded(status.name)
    else:
        print(status.name, 'failed')


async def print_movie_list(movie_list, update: Update, context: ContextTypes.DEFAULT_TYPE):
    for movie in movie_list:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ID: {}\nNAME: {}\nSTATUS: {}\n".format(movie[0], movie[1], "downloaded" if movie[2] == 1 else "uploading - {}%".format(movie[3])))
