from pymongo import MongoClient
from bot import DATABASE_URL, BOT_NAME


client = MongoClient(DATABASE_URL)
db = f'client.aeonfilestore_{BOT_NAME}'
user_data = db.users

async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find({})
    user_ids = []
    for doc in user_docs:
        user_id = doc.get('_id')
        if isinstance(user_id, int):
            user_ids.append(user_id)
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return
