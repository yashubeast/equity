import os
import discord
from discord import Interaction
from discord.app_commands import check
from discord.ext import commands
from dotenv import load_dotenv

from utils.error import NotAdmin

load_dotenv()

# serverID = discord.Object(id=os.environ["ServerID"])
serverID = int(os.environ["ServerID"])
apiLink = os.environ["apiLink"]

admins = set(map(int, os.getenv("admin_list", "").split(",")))
def is_admin():
    @check
    async def predicate(itx: Interaction):
        if itx.user.id not in admins:
            raise NotAdmin()
        return True
    return predicate
