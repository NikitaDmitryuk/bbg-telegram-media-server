import logging
from telegram.ext import ApplicationBuilder

from handlers import application_handlers
import config
import db_utils

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
    db_utils.connection()
    get_application(config.TOKEN).run_polling()


if __name__ == '__main__':
    main()
