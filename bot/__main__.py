import re
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from bot import LOGGER, bot
from bot.modules import in_channel
from bot.helpers.database import add_user, present_user
from bot.helpers.pyro import ButtonMaker, sendMessage
from bot.helpers.encryption import decrypt

help_msg = "Hello"
start_msg = "Hello"

def extract_ids(url):
    pattern = r"https://t\.me/c/(\d+)/(\d+)"
    match = re.match(pattern, url)
    if match:
        chat_id, message_id = match.groups()
        return int(chat_id), int(message_id)
    return None, None

async def help_command(_, message):
    await sendMessage(message, help_msg)

async def start_command(_, message):
    if message.chat.type == "private":
        user_id = message.from_user.id
        if not await present_user(user_id):
            await add_user(user_id)

    if len(message.command) > 1 and len(message.command[1]) > 10:
        link = message.command[1]
        link = decrypt(link)
        cid, mid = extract_ids(link)
        if cid and mid:
            cid = int(f"-100{cid}")
            await bot.copy_message(message.chat.id, cid, mid)
            return

    await sendMessage(message, start_msg)


async def main():
    bot.add_handler(MessageHandler(start_command, filters.command('start')))
    bot.add_handler(MessageHandler(help_command, filters.command('help')))
    LOGGER.info("Bot Started!")


bot.loop.run_until_complete(main())
bot.loop.run_forever()
