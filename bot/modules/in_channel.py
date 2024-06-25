import asyncio
import re

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

from bot import bot, ADMINS, BOT_NAME, STORE_CHANNEL
from bot.helpers.encryption import encrypt

def extract_message_id(url):
    pattern = r"https://t\.me/c/\d+/\d+"
    if re.match(pattern, url):
        message_id = url.split('/')[-1]
        return message_id
    return None

async def copy_message(message):
    try:
        print("Attempting to copy message...")
        post_message = await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
        print(f"Message copied successfully: {post_message}")
        return post_message
    except FloodWait as e:
        print(f"FloodWait error, waiting for {e.x} seconds")
        await asyncio.sleep(e.x)
        try:
            post_message = await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
            print(f"Message copied successfully after FloodWait: {post_message}")
            return post_message
        except Exception as e:
            print(f"Error during message copy after FloodWait: {e}")
            return None
    except Exception as e:
        print(f"Error during message copy: {e}")
        return None

async def channel_post(client, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    post_message = await copy_message(message)
    if not post_message:
        await reply_text.edit_text("Something went wrong during message copy..!")
        return

    if not hasattr(post_message, 'link'):
        await reply_text.edit_text("Something went wrong, no link found in the post_message..!")
        return

    mid = extract_message_id(post_message.link)
    if not mid:
        await reply_text.edit_text("Something went wrong, unable to extract message ID from link..!")
        return

    try:
        base64_string = encrypt(mid)
        link = f"https://t.me/{BOT_NAME}?start={base64_string}"
        await reply_text.edit(
            f"<b>Here is your link</b>\n\noriginal link:\n<code>{link}</code>",
        )
    except Exception as e:
        print(f"Error during encryption or link generation: {e}")
        await reply_text.edit_text("Something went wrong during link generation..!")
        return

private_and_admins_filter = filters.private & ~filters.command(['start', 'users', 'broadcast', 'batch'])
channel_post_handler = MessageHandler(channel_post, private_and_admins_filter)
bot.add_handler(channel_post_handler)