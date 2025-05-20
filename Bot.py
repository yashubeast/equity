import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()


class EconomyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", case_insensitive=True, help_command=None, intents=intents
        )

    async def setup_hook(self):
        for ext in os.listdir("./cogs"):
            if ext.endswith(".py"):
                await bot.load_extension(f"cogs.{ext[:-3]}")
                print(ext)
        await bot.tree.sync()

    async def on_ready(self):
        print(f"Connected to {self.user}")
        print(discord.__version__)


if __name__ == "__main__":

    bot = EconomyBot()
    bot.run(os.getenv("Token"))
