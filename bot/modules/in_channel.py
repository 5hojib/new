import asyncio
import re

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler
from urllib.parse import quote
from cloudscraper import create_scraper

from bot import bot, BOT_NAME, STORE_CHANNEL
from bot.helpers.telegram_utils import sendMessage, copyMessage, editMessage
from bot.helpers.encryption import encrypt
from bot.helpers.filters import Filters


# Configuration
SHORTENERS = {
    "https://modijiurl.com": "cd5b3b10ed0e7c30e795e7ab3c8778f799cafb5b",
    "https://shorturllinks.com": "2bee326db06f49edd14d8f27d24594e260cc2b6f"
}


async def generate_shortened_message(link):
    msgs = [f"Here is the original link: {link}\n"]
    for shortener, api_key in SHORTENERS.items():
        try:
            res = create_scraper().get(f'{shortener}/api?api={api_key}&url={quote(link)}').json()
            short_url = res.get('shortenedUrl', 'failed to shorten')
        except:
            short_url = 'failed to shorten'
        msgs.append(f"Shortened link ({shortener}): {short_url}\n")
    return msgs


def extract_message_id(url):
    match = re.match(r"https://t\.me/c/\d+/\d+", url)
    return url.split('/')[-1] if match else None


async def copy_to_store_channel(message):
    while True:
        try:
            return await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except:
            return None


async def handle_post(_, message):
    reply_msg = await sendMessage(message, "Please wait...")
    copied_msg = await copy_to_store_channel(message)
    if not copied_msg or not hasattr(copied_msg, 'link'):
        return await editMessage(reply_msg, "Failed to copy message or find link.")

    msg_id = extract_message_id(copied_msg.link)
    enc_id = encrypt(msg_id)
    link = f"https://t.me/{BOT_NAME}?start={enc_id}"
    shortened_msg = await generate_shortened_message(link)
    formatted_msg = "\n".join(shortened_msg)
    await editMessage(reply_msg, f"<b>Here is your link</b>\n\n{formatted_msg}")

async def handle_batch(_, message):
    reply_msg = await sendMessage(message, "Please wait...")
    ids = [extract_message_id(part.strip()) for part in message.text.split()[1:3]]
    if None in ids:
        return await editMessage(reply_msg, "Invalid message URLs provided.")

    enc_data = encrypt('_'.join(ids))
    link = f"https://t.me/{BOT_NAME}?start={enc_data}"
    shortened_msg = await generate_shortened_message(link)
    formatted_msg = "\n".join(shortened_msg)
    await editMessage(reply_msg, f"<b>Here is your link</b>\n\n{formatted_msg}")


# Handlers
private_admin_filter = filters.private & Filters.admin & ~filters.command(['start', 'users', 'broadcast', 'batch'])
bot.add_handler(MessageHandler(handle_post, private_admin_filter))
bot.add_handler(MessageHandler(handle_batch, filters.private & Filters.admin & filters.command('batch')))
