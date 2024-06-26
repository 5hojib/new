import asyncio

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from bot import LOGGER, bot, STORE_CHANNEL
from bot.modules import in_channel
from bot.helpers.database import add_user, present_user
from bot.helpers.pyro import ButtonMaker, sendMessage
from bot.helpers.encryption import decrypt


async def start_command(_, message):
    if message.chat.type == "private":
        user_id = message.from_user.id
        if not await present_user(user_id):
            await add_user(user_id)

    if len(message.command) > 1 and len(message.command[1]) > 10:
        encrypted_string = message.command[1]
        decrypted_string = decrypt(encrypted_string)

        if '_' in decrypted_string:
            start_id, end_id = map(int, decrypted_string.split('_'))
            for message_id in range(start_id, end_id + 1):
                await bot.copy_message(message.chat.id, STORE_CHANNEL, message_id)
                await asyncio.sleep(0.5)
        else:
            message_id = int(decrypted_string)
            await bot.copy_message(message.chat.id, STORE_CHANNEL, message_id)
        return

    await sendMessage(message, "Hello\n\nI can store private files in Specified Channel and other users can access it from special link.")


async def main():
    bot.add_handler(MessageHandler(start_command, filters.command('start')))
    LOGGER.info("Bot Started!")


bot.loop.run_until_complete(main())
bot.loop.run_forever()
