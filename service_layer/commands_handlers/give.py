from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def give_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message.reply_to_message is None:
        text = "Please use this command replying to the a message sent by the user whom you want to give coins to"
        update.effective_message.reply_text(text=text, quote=True)

    if len(context.args) < 1:
        text = "Please specify the ammount of coins you want to give"
        update.effective_message.reply_text(text=text, quote=True)

    try:
        int(context.args[0])
    except ValueError:
        text = "Please specify an integer value of coins"
        update.effective_message.reply_text(text=text, quote=True)

    ammount = int(context.args[0])
    from_user_id = update.effective_user.id
    to_user_id = update.effective_message.reply_to_message.from_user.id

    from_fullname = update.effective_user.full_name
    to_fullname = update.effective_message.reply_to_message.from_user.full_name

    with uow:
        from_user_coin_ammount = uow.repo.get_coins(from_user_id)
        to_user_coin_ammount = uow.repo.get_coins(to_user_id)

        if from_user_coin_ammount < ammount:
            text = f"Couldn't give {ammount} coins to {to_fullname}.\nYou only have {from_user_coin_ammount} coins"
            update.effective_message.reply_text(text=text, quote=True)
            return
        
        uow.repo.give_coins(from_user_id, to_user_id, ammount)

        
        from_new_coin_ammount = uow.repo.get_coins(from_user_id)
        to_new_coin_ammount = uow.repo.get_coins(to_user_id)

        text = f"You gave {ammount} coins to {to_fullname}.\n\n{to_fullname}: {to_new_coin_ammount}(+{ammount})\n{from_fullname}: {from_new_coin_ammount}(-{ammount})"
        update.effective_message.reply_text(text=text, quote=True)
        uow.commit()
    
    
