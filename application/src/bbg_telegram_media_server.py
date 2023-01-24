import logging
from telegram.ext import ApplicationBuilder

from handlers import application_handlers
import global_variable
import sqlite_utils

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_application(token: str):
    application = ApplicationBuilder().token(token).build()

    for handler in application_handlers:
        application.add_handler(handler)

    return application


def main():
    global_variable.init_global_variable()
    sqlite_utils.connection()
    get_application(global_variable.get_token()).run_polling()
