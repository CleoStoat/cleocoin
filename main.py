from telethon.sync import TelegramClient
import datetime
import logging
from functools import partial

from telegram.ext import Updater, dispatcher
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

import config
from adapters.orm import create_tables, start_mappers
from bot_commands import COMMANDS
from helpers.command_helpers import set_bot_commands
from service_layer.unit_of_work import SqlAlchemyUnitOfWork


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    start_mappers()
    create_tables()

    updater = Updater(token=config.get_bot_token())

    # Instantiate SqlAlchemy Unit of Work
    uow = SqlAlchemyUnitOfWork()

    set_bot_commands(COMMANDS, updater, uow)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
