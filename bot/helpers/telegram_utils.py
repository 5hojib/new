from asyncio import sleep

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ReplyMarkupInvalid, FloodWait, RPCError, MessageNotModified, MessageEmpty

from bot import LOGGER, bot


async def copyMessage(chat_id, from_chat_id, message_id):
    while True:
        try:
            await bot.copy_message(chat_id, from_chat_id, message_id)
            break
        except FloodWait as e:
            sleep_duration = e.value * 1.1
            LOGGER.warning(f"FloodWait: Sleeping for {sleep_duration:.2f} seconds before retrying...")
            await sleep(sleep_duration)
        except Exception as e:
            LOGGER.error(f"Failed to copy message: {e}")
            raise


async def sendMessage(message, text, buttons=None):
    try:
        return await message.reply(text=text, quote=True, disable_web_page_preview=True, disable_notification=True, reply_markup=buttons)
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(message, text, buttons)
    except ReplyMarkupInvalid:
        return await sendMessage(message, text, None)
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def editMessage(message, text, buttons=None):
    try:
        if message.media:
            return await message.edit_caption(caption=text, reply_markup=buttons)
        await message.edit(text=text, disable_web_page_preview=True, reply_markup=buttons)
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await editMessage(message, text, buttons)
    except (MessageNotModified, MessageEmpty):
        pass
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def deleteMessage(message):
    try:
        await message.delete()
    except Exception as e:
        LOGGER.error(str(e))


class ButtonMaker:
    def __init__(self):
        self._button = []

    def url(self, key, link):
        self._button.append(
            InlineKeyboardButton(
                text=key,
                url=link
            )
        )

    def click(self, key, data):
        self._button.append(
            InlineKeyboardButton(
                text=key,
                callback_data=data
            )
        )

    def build_menu(self, column=1):
        menu = [self._button[i : i + column] for i in range(0, len(self._button), column)]
        return InlineKeyboardMarkup(menu)
