import json 

from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def coinstatus_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    user_id = update.effective_user.id
    with uow:
        coin_ammount = uow.repo.get_coins(user_id=user_id)
        text = f"You currently have {coin_ammount} coins"
        update.effective_message.reply_text(text=text, quote=True)
        uow.commit()
    
    
