from pyrogram.filters import create

from bot import ADMINS


class Filters:
    async def admins(self, _, message):
        return bool(message.from_user.id in ADMINS)
    admin = create(admins)
