import asyncio

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

from bot import LOGGER, bot, STORE_CHANNEL
from bot.modules import in_channel
from bot.helpers.database import add_user, is_user_present
from bot.helpers.telegram_utils import sendMessage, copyMessage
from bot.helpers.encryption import decrypt


async def handle_start_command(_, message):
    if message.chat.type == "private" and not await is_user_present(message.from_user.id):
        await add_user(message.from_user.id)

    if len(message.command) > 1 and len(message.command[1]) > 10:
        decrypted_string = decrypt(message.command[1])
        if '_' in decrypted_string:
            try:
                start_id, end_id = map(int, decrypted_string.split('_'))
                for message_id in range(start_id, end_id + 1):
                    await copyMessage(message.chat.id, STORE_CHANNEL, message_id)
                    await asyncio.sleep(0.5)
            except ValueError:
                await sendMessage(message, "Invalid command format. Please try again.")
        else:
            try:
                await copyMessage(message.chat.id, STORE_CHANNEL, int(decrypted_string))
            except ValueError:
                await sendMessage(message, "Invalid command format. Please try again.")
    else:
        await sendMessage(message, "Hello\n\nI can store private files in a specified channel, and other users can access them from a special link.")

async def main():
    bot.add_handler(MessageHandler(handle_start_command, filters.command('start')))
    LOGGER.info("Bot Started!")

bot.loop.run_until_complete(main())
bot.loop.run_forever()
