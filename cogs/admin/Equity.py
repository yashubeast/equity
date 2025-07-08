import os
import aiohttp

import discord
from discord import app_commands, Interaction
from discord.ext import commands
from utils.logger import log
from utils.lib import serverID, apiLink, is_admin

class Equity(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    eq = app_commands.Group(
        name='eq',
        description='admin only equity commands',
        default_permissions=discord.Permissions(administrator=True),
        guild_ids=[serverID]
    )

    @is_admin()
    @eq.command(name="balance", description="Check Equity balance of user")
    async def balance(self, itx: discord.Interaction, user: discord.Member):

        await itx.response.defer(ephemeral=True, thinking=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{apiLink}/balance",
                json={
                    "user_id": str(user.id)
                }
            ) as resp:
                data = await resp.json()
                if resp.status == 200:
                    log.info(f"eq balance: {user} {data['result']} by {itx.user}")
                else:
                    log.warning(f"eq balance {resp.status}: {user} by {itx.user} => {data['result']}")
                    await itx.edit_original_response(content='Trouble fetching balance')
                    return

        embed = discord.Embed(
            title=f"{user.name}'s Balance", description=f"*User has {data['result']} Equity*"
        )

        embed.set_thumbnail(
            url=user.avatar if user.avatar else user.default_avatar
        )

        embed.set_footer(text=itx.guild.name, icon_url=itx.guild.icon)

        await itx.edit_original_response(embed=embed)

    @is_admin()
    @eq.command(name="penalize", description="Penalize user for Equity")
    @app_commands.describe(
        user = "user to penalize",
        reason = "reason for penalizing (appended to message with a comma)",
        hide = "whether to hide the message or not (True by default)"
    )
    async def penalize(self, itx: discord.Interaction, user: discord.Member, amount: int, reason: str = None, hide: bool = True):

        await itx.response.defer(ephemeral=True, thinking=True)

        sender_id = str(user.id)
        receiver_id = '0'

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{apiLink}/pay",
                json={
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "amount": amount
                }
            ) as resp:
                data = await resp.json()
                if resp.status == 200:
                    log.info(f"eq penalize: {amount} {user} by {itx.user}" + f"{', ' + reason if reason else ''}")
                    await itx.edit_original_response(content=f"Penalized {user.mention} for {amount} Equity",
                        allowed_mentions=discord.AllowedMentions(users=False))
                    if not hide:
                        await itx.channel.send(f"Penalized {user.mention} for {amount} Equity" + f"{', ' + reason if reason else ''}")
                    return
                elif resp.status == 400:
                    log.warning(f"eq penalize {resp.status}: {amount} {user} by {itx.user} => {data['result']}")
                    await itx.edit_original_response(content=data['result'])
                    return
                else:
                    log.warning(f"eq penalize {resp.status}: {amount} {user} by {itx.user} => {data['result']}")
                    await itx.edit_original_response(content=f"Trouble penalizing {user}")
                    return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Equity(bot))
