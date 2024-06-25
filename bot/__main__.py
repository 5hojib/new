from pyrogram.handlers import MessageHandler
from pyrogram.filters import command

from bot import LOGGER, bot

from bot.modules import in_channel
from bot.helpers.database import add_user, present_user
from bot.helpers.pyro import ButtonMaker, sendMessage
from bot.helpers.encryption import decrypt

help_msg = "Hello"
start_msg = "hello"

import re

def extract_ids(url):
    pattern = r"https://t\.me/c/(\d+)/(\d+)"
    match = re.match(pattern, url)
    
    chat_id, message_id = match.groups()
    return int(chat_id), int(message_id)


async def help(_, message):
    await sendMessage(message, help_msg)

async def start(_, message):
    if message.chat.type.BOT:
        user_id = message.from_user.id
        if not await present_user(user_id):
            await add_user(user_id)
    if len(message.command) > 1 and len(message.command[1]) > 10:
        link = message.command[1]
        link = decrypt(link)
        cid, mid = extract_ids(link)
        return await bot.copy_message(message.chat.id, cid, mid)
    await sendMessage(message, start_msg)

async def main():
    bot.add_handler(MessageHandler(start, filters=command('start')))
    bot.add_handler(MessageHandler(help, filters=command('help')))
    LOGGER.info("Bot Started! x")


bot.loop.run_until_complete(main())
bot.loop.run_forever()
