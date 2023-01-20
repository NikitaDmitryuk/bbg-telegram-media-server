import sqlite3
import os

import global_variable

def create_db(path_database):
    conn = sqlite3.connect(path_database)
    conn.execute('''CREATE TABLE Movie 
                (ID             INTEGER         NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                NAME            TEXT        NOT NULL,
                UPLOADED_FILE   TEXT        NOT NULL,
                TORRENT_FILE    TEXT        NOT NULL,
                LOADED          BOOLEAN     NOT NULL        DEFAULT 0       CHECK (LOADED IN (0, 1))
                );''')
    conn.commit()
    return conn

def connection():
    path_database = os.path.join(global_variable.PATH_TO_SAVE_TORRENT_FILE, 'movie.db')
    if os.path.exists(path_database):
        return sqlite3.connect(path_database)
    else:
        return create_db(path_database)

def add_movie(name, uploaded_file_name, torrent_file_name):
    conn = connection()
    cur = conn.cursor()
    cur.execute('''INSERT INTO Movie (NAME, UPLOADED_FILE, TORRENT_FILE)
                VALUES ('{name}', '{uploaded_file}', '{torrent_file}')
                '''.format(name=name, uploaded_file=uploaded_file_name, torrent_file=torrent_file_name)
                )
    conn.commit()
    conn.close()

def set_loaded(name):
    conn = connection()
    cur = conn.cursor()
    cur.execute('''UPDATE Movie
                    SET LOADED = 1
                    WHERE NAME = '{name}'
                '''.format(name=name)
                )
    conn.commit()
    conn.close()

def remove_movie(name):
    conn = connection()
    cur = conn.cursor()
    cur.execute('''DELETE FROM Movie
                    WHERE NAME = '{name}'
                '''.format(name=name)
                )
    conn.commit()
    conn.close()
