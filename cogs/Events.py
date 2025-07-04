import os
import datetime
import math
import aiohttp

from discord.ext import commands

from dotenv import load_dotenv

class EventCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.fulfillcontracts.start()

    # @tasks.loop(time=datetime.time(12, 0))  # Executes at 12:00 PM every day
    # async def fulfillcontracts(self):
    #     DB = BankDB()
    #     DB.fulfill_contracts()

    # @fulfillcontracts.before_loop
    # async def before_fulfillcontracts(self):
    #     # Wait until the bot is ready before starting the loop
    #     await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        user = (message.author)
        if message.author.bot:
            return

        user_id = str(user.id)
        message_id = str(message.id)
        message_length = len(message.content)
        timestamp = str(datetime.datetime.utcnow().timestamp())

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{os.getenv('magi')}/eval",
                json={
                    "user_id": user_id,
                    "message_id": message_id,
                    "message_length": message_length,
                    "timestamp": timestamp,
                }
            ) as resp:
                data = await resp.json()
                if resp.status == 200:
                    print(f'eval: {user}, {message_id} -> +{data['result']}')
                else:
                    print(f"eval error: {resp.status} {data}")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        
        message_id = str(payload.message_id)

        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{os.getenv('magi')}/del",
                json={
                    "message_id": message_id,
                }
            ) as resp:
                data = await resp.json()
                if resp.status == 200:
                    print(f'del: {message_id} -> -{data['result']}')
                else:
                    print(f"del error {resp.status}: {data['result']}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventCog(bot))
