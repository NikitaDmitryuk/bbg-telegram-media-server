import os
import shutil

import libtorrent as lt
from telegram import Update
from telegram.ext import ContextTypes
import aiofiles.os as aioos
import asyncio

import global_variable
import sqlite_utils


async def remove(file):

    if await aioos.path.exists(file):
        if await aioos.path.isfile(file) or await aioos.path.islink(file):
            await aioos.remove(file)
        elif await aioos.path.isdir(file):
            shutil.rmtree(file)
        else:
            raise ValueError("Undefined file format {}".format(file))
    else:
        raise ValueError("file {} not exists.".format(file))


async def download_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE, file_id):
    full_file = os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, file_id)
    info = lt.torrent_info(full_file)
    session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    handle = session.add_torrent({'ti': info, 'save_path': global_variable.PATH_TO_SAVE_TORRENT_FILE})
    status = handle.status()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="starting \"{}\"".format(status.name))
    print('starting', status.name)
    sqlite_utils.add_movie(status.name, status.name, file_id)
    i = 1
    current_time = 0
    time_step = 10
    time_out = 600

    while (not status.is_seeding):
        
        if i == 1 and current_time >= time_out:
            await remove(full_file)
            await remove(os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, status.name))
            await context.bot.send_message(chat_id=update.effective_chat.id, text='\"{}\": time out!'.format(status.name))
            sqlite_utils.remove_movie(status.name)
            session.remove_torrent(handle)
            break

        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
            status.progress * 100, status.download_rate / 1000, status.upload_rate / 1000,
            status.num_peers, status.state), end=' ')

        if round(status.progress * 100) // 10 >= i:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='\"%s\": %.2f%% complete (down: %.1f MB/s up: %.1f kB/s peers: %d)' % (handle.status().name, status.progress * 100, status.download_rate / 1048576, status.upload_rate / 1024, status.num_peers))
            i += 1

        alerts = session.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)

        await asyncio.sleep(time_step)
        current_time += time_step
        status = handle.status()
    
    return status


async def print_movie_list(movie_list, update: Update, context: ContextTypes.DEFAULT_TYPE):
    for movie in movie_list:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="ID: {}\nNAME: {}\nSTATUS: {}\n".format(movie[0], movie[1], "downloaded" if movie[2] == 1 else "loading"))
