import datetime
import motor.motor_asyncio
from config import Config
from .utils import send_log


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.date.today().isoformat(),
            posts=[],
            buttons=[],
            channels=[]
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_posts(self, user_id, post):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            posts = user.get('posts', [])
            posts.append(post)
            await self.col.update_one({'id': int(user_id)}, {'$set': {'posts': posts}})

    async def get_posts(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('posts', [])

    async def del_post(self, user_id, post):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            posts = user.get('posts', [])
            posts.remove(post)
            await self.col.update_one({'id': int(user_id)}, {'$set': {'posts': posts}})

    async def set_buttons(self, user_id, button):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            buttons = user.get('buttons', [])
            buttons.append(button)
            await self.col.update_one({'id': int(user_id)}, {'$set': {'buttons': buttons}})

    async def get_buttons(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('buttons', [])

    async def del_button(self, user_id, button):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            buttons = user.get('buttons', [])
            buttons.pop(button)
            await self.col.update_one({'id': int(user_id)}, {'$set': {'buttons': buttons}})

    async def set_channels(self, user_id, channel):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            channels = user.get('channels', [])
            channels.append(channel)
            await self.col.update_one({'id': int(user_id)}, {'$set': {'channels': channels}})

    async def get_channels(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('channels', [])

    async def del_channel(self, user_id, channel):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            channels = user.get('channels', [])
            channels.remove(channel)
            await self.col.update_one({'id': int(user_id)}, {'$set': {'channels': channels}})


db = Database(Config.DB_URL, Config.BOT_USERNAME)
