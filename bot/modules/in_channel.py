import asyncio
import re

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

from bot import bot, ADMINS, BOT_NAME, STORE_CHANNEL
from bot.helpers.encryption import encrypt
from bot.helpers.filters import Filters


def extract_message_id(url):
    pattern = r"https://t\.me/c/\d+/\d+"
    match = re.match(pattern, url)
    return url.split('/')[-1] if match else None

async def copy_message(message):
    while True:
        try:
            post_message = await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
            return post_message
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            return None

async def channel_post(client, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    post_message = await copy_message(message)
    
    if not post_message or not hasattr(post_message, 'link'):
        await reply_text.edit_text("Something went wrong, unable to copy message or find link!")
        return

    mid = extract_message_id(post_message.link)
    if not mid:
        await reply_text.edit_text("Something went wrong, unable to extract message ID from link!")
        return

    string = encrypt(mid)
    link = f"https://t.me/{BOT_NAME}?start={string}"
    await reply_text.edit(f"<b>Here is your link</b>\n\noriginal link:\n<code>{link}</code>")

async def batch(_, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    msg = message.text.split()
    first_id = extract_message_id(msg[1].strip())
    second_id = extract_message_id(msg[2].strip())

    if not first_id or not second_id:
        await reply_text.edit_text("Invalid message URLs provided.")
        return

    data = f"{first_id}_{second_id}"
    string = encrypt(data)
    link = f"https://t.me/{BOT_NAME}?start={string}"
    await reply_text.edit(f"<b>Here is your link</b>\n\noriginal link:\n<code>{link}</code>")


# Handlers
private_and_admins_filter = filters.private & Filters.admin & ~filters.command(['start', 'users', 'broadcast', 'batch'])
channel_post_handler = MessageHandler(channel_post, private_and_admins_filter)
batch_handler = MessageHandler(batch, filters.private & Filters.admin & filters.command('batch'))

bot.add_handler(channel_post_handler)
bot.add_handler(batch_handler)
