
from typing import Optional
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config
from helpers.telethon_helpers import get_id_by_username

def find_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if len(context.args) < 1:
        text = "Please specify the username"
        update.effective_message.reply_text(text=text, quote=True)
        return

    username = context.args[0].removeprefix("@")
    
    user_id: Optional[int] = get_id_by_username(username)

    if user_id is None:
        text = f"Couldn't find user with username @{username}"
        update.effective_message.reply_text(text=text, quote=True)
        return
    
    text = f"@{username} id:\n{user_id}"
    update.effective_message.reply_text(text=text, quote=True)

    
    