import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

from bot import bot, ADMINS, BOT_NAME, STORE_CHANNEL
from bot.helpers.encryption import encrypt

async def channel_post(client, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=STORE_CHANNEL, disable_notification=True)
    except Exception as e:
        print(f"Error during message copy: {e}")
        await reply_text.edit_text("Something went Wrong..!")
        return

    try:
        base64_string = encrypt(post_message.link)
    except Exception as e:
        print(f"Error during encryption: {e}")
        await reply_text.edit("Encryption failed..!")
        return

    link = f"https://t.me/{BOT_NAME}?start={base64_string}"

    await reply_text.edit(
        f"<b>Here is your link</b>\n\noriginal link:\n<code>{link}</code>",
        parse_mode="html"
    )

private_and_admins_filter = filters.private & ~filters.command(['start','users','broadcast','batch','genlink','stats'])

channel_post_handler = MessageHandler(channel_post, private_and_admins_filter)
bot.add_handler(channel_post_handler)
