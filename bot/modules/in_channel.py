from pyrogram import filters
from pyrogram.errors import FloodWait

from bot import bot, ADMINS, BOT_NAME, STORE_CHANNEL
from bot.helpers.encryption import encrypt


@bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(_, message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = STORE_CHANNEL, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = STORE_CHANNEL, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    base64_string = encrypt(post_message.link)
    link = f"https://t.me/{BOT_NAME}?start={base64_string}"

    await reply_text.edit(
        f"<b>Here is your link</b>\n\noriginal link:\n<blockquote><code>{link}</code>")