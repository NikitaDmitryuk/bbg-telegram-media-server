import os
import sqlite3

from . import config


def create_db(path_database: str):
    connect_db = sqlite3.connect(path_database)
    connect_db.execute(
        """CREATE TABLE Movie
                (ID                     INTEGER     NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                NAME                    TEXT        NOT NULL,
                UPLOADED_FILE           TEXT        NOT NULL,
                TORRENT_FILE            TEXT        NOT NULL,
                DOWNLOADED_PERCENTAGE   INTEGER     NOT NULL        DEFAULT 0       CHECK (DOWNLOADED_PERCENTAGE BETWEEN 0 AND 100),
                DOWNLOADED              BOOLEAN     NOT NULL        DEFAULT 0       CHECK (DOWNLOADED IN (0, 1))
                );"""
    )

    connect_db.execute(
        """CREATE TABLE User
                (ID             INTEGER         NOT NULL        PRIMARY KEY     AUTOINCREMENT,
                NAME            TEXT            NOT NULL,
                CHAT_ID         INTEGER         NOT NULL
                );"""
    )
    connect_db.commit()
    return connect_db


def connection():
    path_database = os.path.join(config.PATH_TO_SAVE_TORRENT_FILE, "movie.db")
    if os.path.exists(path_database):
        return sqlite3.connect(path_database)
    else:
        return create_db(path_database)


conn = connection()
cur = conn.cursor()


def add_movie(name: str, uploaded_file_name: str, torrent_file_name: str) -> None:
    cur.execute(
        f"""INSERT INTO Movie (NAME, UPLOADED_FILE, TORRENT_FILE)
                VALUES ('{name}', '{uploaded_file_name}', '{torrent_file_name}')
                """
    )
    conn.commit()


def set_loaded(name: str) -> None:
    cur.execute(
        f"""UPDATE Movie
                    SET DOWNLOADED = 1
                    WHERE NAME = '{name}'
                """
    )
    conn.commit()


def get_movie_by_id(movie_id: int):
    res = cur.execute(
        f"""SELECT NAME, UPLOADED_FILE, TORRENT_FILE FROM Movie 
                    WHERE ID = {movie_id}"""
    )
    movie_files = res.fetchall()
    return movie_files[0] if movie_files else None


def remove_movie(movi_id: int) -> None:
    cur.execute(
        f"""DELETE FROM Movie
                    WHERE ID = {movi_id}
                """
    )
    conn.commit()


def get_movie_list():
    res = cur.execute("""SELECT ID, NAME, DOWNLOADED, DOWNLOADED_PERCENTAGE FROM Movie ORDER BY ID""")
    list_of_movie = res.fetchall()
    return list_of_movie


def login(password: str, chat_id: int, user_name: str):
    if password == config.PASSWORD:
        cur.execute(
            f"""INSERT INTO User (NAME, CHAT_ID)
                    VALUES ('{user_name}', {chat_id})
                    """
        )
        conn.commit()
        return True
    else:
        return False


def update_downloaded_percentage(name: str, percentage: int) -> None:
    print(name, percentage)
    cur.execute(
        f"""UPDATE Movie
                    SET DOWNLOADED_PERCENTAGE = {percentage}
                    WHERE NAME = '{name}'
                """
    )
    conn.commit()


def check_user(chat_id: int):
    res = cur.execute(
        f"""SELECT * FROM User
                    WHERE CHAT_ID = {chat_id}
                    """
    )
    check_status = True if res.fetchall() else False
    return check_status


def close_db_connection():
    conn.close()
