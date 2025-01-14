import discord
from discord.ext import commands, tasks
from discord import app_commands
from utils.database import BankDB
import datetime


class EventCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fulfillcontracts.start()

    @tasks.loop(time=datetime.time(12,0))  # Executes at 12:00 PM every day
    async def fulfillcontracts(self):
        DB = BankDB()
        DB.fulfill_contracts()

    @fulfillcontracts.before_loop
    async def before_fulfillcontracts(self):
        # Wait until the bot is ready before starting the loop
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        if message.author.bot:
            return
        current_datetime = datetime.datetime.utcnow()
        DB = BankDB()
        messages = DB.get_messages(user.id)
        lastmessage = DB.get_last_message(user.id)
        bonus = DB.bonus_rate()
        lastmessage = datetime.datetime.strptime(lastmessage, "%Y-%m-%d %H:%M:%S.%f")
        time_difference = (current_datetime - lastmessage).total_seconds()
        time_value = time_difference * .15
        if time_value > 1:
            overflowValue = (time_difference - 7) * .0001
            time_value = 1 + overflowValue
        total = len(message.content) * (1+(bonus*messages)) * time_value
        tax = DB.tax_rate()
        Mastercoins = int(total) * float(tax)
        userCoins = int(total - Mastercoins)
        Mastercoins = total - userCoins + Mastercoins
        DB.event_add(user.id,userCoins,Mastercoins,message)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        DB = BankDB()
        DB.delete_message(payload.message_id)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventCog(bot))