import os
import time

import libtorrent as lt
import shutil
from telegram import Update
from telegram.ext import ContextTypes

import global_variable

async def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

async def download_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE, full_file):
    info = lt.torrent_info(full_file)
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    h = ses.add_torrent({'ti': info, 'save_path': global_variable.PATH_TO_SAVE_TORRENT_FILE})
    s = h.status()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="starting " + s.name)
    print('starting', s.name)
    i = 1
    current_time = 0
    time_step = 10

    while (not s.is_seeding):
        
        if i == 1 and current_time == 600:
            await remove(full_file)
            await remove(os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, h.status().name))
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
        s = h.status()
    
    return s
