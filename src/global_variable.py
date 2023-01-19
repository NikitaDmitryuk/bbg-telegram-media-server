import os
import sys


def init_global_variable():
    global PATH_TO_SAVE_TORRENT_FILE
    global PASSWORD
    global TOKEN

    PATH_TO_SAVE_TORRENT_FILE = sys.argv[1]

    print(PATH_TO_SAVE_TORRENT_FILE)

    with open(os.path.join(PATH_TO_SAVE_TORRENT_FILE, 'Authorization_password.pwd'), 'r') as file:
        PASSWORD = file.readline().replace('\n', '')

    with open(os.path.join(PATH_TO_SAVE_TORRENT_FILE, 'bot.token'), 'r') as file:
        TOKEN = file.readline().replace('\n', '')
