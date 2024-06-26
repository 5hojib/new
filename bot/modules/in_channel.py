import asyncio
import re

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

from bot import bot, ADMINS, BOT_NAME, STORE_CHANNEL
from bot.helpers.pyro import sendMessage, copyMessage, editMessage
from bot.helpers.encryption import encrypt
from bot.helpers.filters import Filters


def extract_message_id_from_url(url):
    pattern = r"https://t\.me/c/\d+/\d+"
    match = re.match(pattern, url)
    return url.split('/')[-1] if match else None

async def copy_message_to_store_channel(message):
    while True:
        try:
            copied_message = await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
            return copied_message
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            return None

async def handle_channel_post(client, message):
    reply_message = await sendMessage(message, "Please wait...")
    copied_message = await copy_message_to_store_channel(message)
    
    if not copied_message or not hasattr(copied_message, 'link'):
        await editMessage(reply_message, "Something went wrong, unable to copy message or find link!")
        return

    message_id = extract_message_id_from_url(copied_message.link)
    if not message_id:
        await editMessage(reply_message, "Something went wrong, unable to extract message ID from link!")
        return

    encrypted_id = encrypt(message_id)
    generated_link = f"https://t.me/{BOT_NAME}?start={encrypted_id}"
    await editMessage(reply_message, f"<b>Here is your link</b>\n\noriginal link:\n<code>{generated_link}</code>")

async def handle_batch_command(_, message):
    reply_message = await sendMessage(message, "Please wait...")
    msg_parts = message.text.split()
    first_message_id = extract_message_id_from_url(msg_parts[1].strip())
    second_message_id = extract_message_id_from_url(msg_parts[2].strip())

    if not first_message_id or not second_message_id:
        await editMessage(reply_message, "Invalid message URLs provided.")
        return

    concatenated_ids = f"{first_message_id}_{second_message_id}"
    encrypted_data = encrypt(concatenated_ids)
    generated_link = f"https://t.me/{BOT_NAME}?start={encrypted_data}"
    await editMessage(reply_message, f"<b>Here is your link</b>\n\noriginal link:\n<code>{generated_link}</code>")


# Handlers
private_and_admin_filter = filters.private & Filters.admin & ~filters.command(['start', 'users', 'broadcast', 'batch'])
channel_post_message_handler = MessageHandler(handle_channel_post, private_and_admin_filter)
batch_command_handler = MessageHandler(handle_batch_command, filters.private & Filters.admin & filters.command('batch'))

bot.add_handler(channel_post_message_handler)
bot.add_handler(batch_command_handler)
