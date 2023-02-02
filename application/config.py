#!python
#cython: language_level=3

import os
import sys

PATH_TO_SAVE_TORRENT_FILE = sys.argv[1]

with open(os.path.join(PATH_TO_SAVE_TORRENT_FILE, 'password.txt'), 'r') as file:
    PASSWORD = file.readline().replace('\n', '')

with open(os.path.join(PATH_TO_SAVE_TORRENT_FILE, 'token.txt'), 'r') as file:
    TOKEN = file.readline().replace('\n', '')
