import os
import discord

from dotenv import load_dotenv

load_dotenv()

# serverID = discord.Object(id=os.environ["ServerID"])
serverID = int(os.environ["ServerID"])
apiLink = os.environ["apiLink"]
