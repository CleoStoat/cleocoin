import asyncio
from typing import Optional

import config

def get_id_by_username(username: str) -> Optional[int]:
    
    from telethon.sync import TelegramClient
    api_id = config.get_api_id()
    api_hash = config.get_api_hash()
    bot_token = config.get_bot_token()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    username = username.removeprefix("@")
    with bot:
        try:
            someone = bot.get_entity(username)
            return someone.id
        except Exception:
            return None