import re

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from bot import LOGGER, bot, STORE_CHANNEL
from bot.modules import in_channel
from bot.helpers.database import add_user, present_user
from bot.helpers.pyro import ButtonMaker, sendMessage
from bot.helpers.encryption import decrypt


#async def help_command(_, message):
 #   await sendMessage(message, help_msg)

async def start_command(_, message):
    if message.chat.type == "private":
        user_id = message.from_user.id
        if not await present_user(user_id):
            await add_user(user_id)

    if len(message.command) > 1 and len(message.command[1]) > 10:
        string = message.command[1]
        message_id = int(decrypt(string))
        await bot.copy_message(message.chat.id, STORE_CHANNEL, message_id)
        return

    await sendMessage(message, "Hello\n\nI can store private files in Specified Channel and other users can access it from special link.")


async def main():
    bot.add_handler(MessageHandler(start_command, filters.command('start')))
    #bot.add_handler(MessageHandler(help_command, filters.command('help')))
    LOGGER.info("Bot Started!")


bot.loop.run_until_complete(main())
bot.loop.run_forever()
