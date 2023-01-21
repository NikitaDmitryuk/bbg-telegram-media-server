import sqlite3
import os

import global_variable

def create_db(path_database):
    conn = sqlite3.connect(path_database)
    conn.execute('''CREATE TABLE Movie 
                (ID             INTEGER     NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                NAME            TEXT        NOT NULL,
                UPLOADED_FILE   TEXT        NOT NULL,
                TORRENT_FILE    TEXT        NOT NULL,
                DOWNLOADED      BOOLEAN     NOT NULL        DEFAULT 0       CHECK (DOWNLOADED IN (0, 1))
                );''')

    conn.execute('''CREATE TABLE User
                (ID             INTEGER         NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                NAME            TEXT            NOT NULL,
                CHAT_ID         INTEGER         NOT NULL
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
                    SET DOWNLOADED = 1
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

def get_movie_list():
    conn = connection()
    cur = conn.cursor()
    res = cur.execute('''SELECT ID, NAME, DOWNLOADED FROM Movie ORDER BY ID''')
    list_of_movie = res.fetchall()
    conn.close()
    return list_of_movie

def login(password, chat_id, user_name):
    if password == global_variable.PASSWORD:
        conn = connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO User (NAME, CHAT_ID)
                    VALUES ('{user_name}', {chat_id})
                    '''.format(user_name=user_name, chat_id=chat_id)
                    )
        conn.commit()
        conn.close()
        return True
    else:
        return False

def check_user(chat_id):
    conn = connection()
    cur = conn.cursor()
    res = cur.execute('''SELECT * FROM User
                    WHERE CHAT_ID = {chat_id}
                    '''.format(chat_id=chat_id)
                    )
    check_status = True if len(res.fetchall()) > 0 else False
    conn.close()
    return check_status
