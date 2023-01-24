import os
import sys

path_to_save_torrent_file = ''
password = ''
token = ''


def init_global_variable():
    global path_to_save_torrent_file
    global password
    global token

    path_to_save_torrent_file = sys.argv[1]

    with open(os.path.join(path_to_save_torrent_file, 'password.txt'), 'r') as file:
        password = file.readline().replace('\n', '')

    with open(os.path.join(path_to_save_torrent_file, 'token.txt'), 'r') as file:
        token = file.readline().replace('\n', '')


def get_path_to_save_torrent_file():
    return path_to_save_torrent_file


def get_token():
    return token


def get_password():
    return password
