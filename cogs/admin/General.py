from discord.ext.commands import Context
import discord


class General(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name='say', help='make bot send a message')
	@commands.has_permissions(administrator=True)
	@commands.bot_has_permissions(manage_messages=True)
	async def say(self, ctx: Context, *, message: str = None):
		files = [await att.to_file() for att in ctx.message.attachments]

		if not message and not files:
			await ctx.send(
				"> requires atleast a message or a attachment\n> -# deleting...",
				delete_after=5
			)
			return

		await ctx.send(
			content = message,
			files = files,
			reference = ctx.message.reference if ctx.message.reference else None
		)
		try:
			await ctx.message.delete()
		except discord.Forbidden:
			pass

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(General(bot))