import os

from discord.ext import commands
from utils.logger import log

async def load_all_cogs(bot):
	for root, _, files in os.walk("./cogs"):
		for file in files:
			if file.endswith(".py"):
				# get module path, e.g. cogs/admin/mod.py -> cogs.admin.mod
				rel_path = os.path.relpath(os.path.join(root, file), ".")
				module_path = rel_path[:-3].replace(os.path.sep, ".")

				try:
					await bot.unload_extension(module_path)
				except commands.ExtensionNotLoaded:
					pass
				await bot.load_extension(module_path)
				log.info("loaded %s", module_path)
