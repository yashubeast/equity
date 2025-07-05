import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import log
from utils.cogs import load_all_cogs

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()

class EconomyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", case_insensitive=True, help_command=None, intents=intents
        )

    async def setup_hook(self):
        await load_all_cogs(self)
        await bot.tree.sync()

    async def on_ready(self):
        log.info("connected as %s", self.user)
        log.info("discord.py version %s", discord.__version__)

if __name__ == "__main__":

    bot = EconomyBot()
    bot.run(os.environ["Token"])
