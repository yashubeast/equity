from math import e
import os
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import log
from utils.lib import apiLink

load_dotenv()

# @app_commands.guild_only()
# @app_commands.default_permissions(administrator=True)
# class AdminContractGroup(
#     commands.GroupCog, name="admincontract", description="Create/Manage contracts with other users"
# ):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot
#
#     @app_commands.command(name="create", description="Create a contract with another user")
#     @app_commands.describe(user="User you wish to create a contract with")
#     @app_commands.describe(length="Length of time for contract in days")
#     @app_commands.describe(amount="Daily amount to be given in the contract")
#     async def contract_create(
#         self, itx: discord.Interaction, user: discord.Member, length: int, amount: int
#     ):
#         DB = BankDB()
#         if 1 > length:
#             await itx.response.send_message(
#                 "You cant create a contract with a length of less than 1 day.", ephemeral=True
#             )
#         DB.contract_add(os.getenv("ServerID"), user.id, amount, length)
#         await itx.response.send_message(f"Admin contract Created for {user}", ephemeral=True)
#
#     @app_commands.command(name="list", description="List of all your current outgoing contracts")
#     async def contract_list(self, itx: discord.Interaction):
#         DB = BankDB()
#         results = DB.list_contracts(os.getenv("ServerID"))
#         if results == []:
#             embed = discord.Embed(title=f"{itx.guild.name}'s Contracts", description="No Contracts")
#             embed.set_thumbnail(
#                 url=itx.user.avatar.url if itx.user.avatar.url else itx.user.default_avatar
#             )
#
#             embed.set_footer(text="Universium", icon_url=itx.guild.icon)
#             await itx.response.send_message(embed=embed, ephemeral=True)
#             return
#         description = ""
#         for result in results:
#             if len(description) > 3980:
#                 continue
#             description += "\n"
#             description += f"{result[0]} - <@{result[2]}> {result[3]} coins * {result[4]} days"
#         embed = discord.Embed(title=f"{itx.guild.name}'s Contracts", description=description)
#         embed.set_thumbnail(
#             url=itx.user.avatar.url if itx.user.avatar.url else itx.user.default_avatar
#         )
#
#         embed.set_footer(text="Universium", icon_url=itx.guild.icon)
#         await itx.response.send_message(embed=embed, ephemeral=True)
#
#     @app_commands.command(name="cancel", description="Cancel an outgoing contract")
#     @app_commands.describe(contract_id="ID listed on the contract")
#     async def contract_delete(self, itx: discord.Interaction, contract_id: int):
#         DB = BankDB()
#         contracts = DB.list_contracts(os.getenv("ServerID"))
#
#         for contract in contracts:
#             if contract[0] == contract_id:
#                 DB.delete_contract(contract_id)
#                 await itx.response.send_message(
#                     f"The Contract with ID {contract_id} for <@{contract[2]}> has been cancelled",
#                     ephemeral=True,
#                 )
#                 return
#         await itx.response.send_message(
#             f"You do not control a contract with ID {contract_id}.", ephemeral=True
#         )

# class ContractGroup(
#     commands.GroupCog, name="contract", description="Create/Manage contracts with other users"
# ):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot
#
#     @app_commands.command(name="create", description="Create a contract with another user")
#     @app_commands.describe(user="User you wish to create a contract with")
#     @app_commands.describe(length="Length of time for contract in days")
#     @app_commands.describe(amount="Daily amount to be given in the contract")
#     async def contract_create(
#         self, itx: discord.Interaction, user: discord.Member, length: int, amount: int
#     ):
#         DB = BankDB()
#         if 1 > length:
#             await itx.response.send_message(
#                 "You cant create a contract with a length of less than 1 day.", ephemeral=True
#             )
#         DB.contract_add(itx.user.id, user.id, amount, length)
#         await itx.response.send_message(
#             f"Contract Created between {user} and yourself", ephemeral=True
#         )
#
#     @app_commands.command(name="list", description="List of all your current outgoing contracts")
#     async def contract_list(self, itx: discord.Interaction):
#         DB = BankDB()
#         results = DB.list_contracts(itx.user.id)
#         if results == []:
#             embed = discord.Embed(title=f"{itx.user}'s Contracts", description="No Contracts")
#             embed.set_thumbnail(
#                 url=itx.user.avatar.url if itx.user.avatar.url else itx.user.default_avatar
#             )
#
#             embed.set_footer(text="Universium", icon_url=itx.guild.icon)
#             await itx.response.send_message(embed=embed, ephemeral=True)
#             return
#         description = ""
#         for result in results:
#             if len(description) > 3980:
#                 continue
#             description += "\n"
#             description += f"{result[0]} - <@{result[2]}> {result[3]} coins * {result[4]} days"
#         embed = discord.Embed(title=f"{itx.user}'s Contracts", description=description)
#         embed.set_thumbnail(
#             url=itx.user.avatar.url if itx.user.avatar.url else itx.user.default_avatar
#         )
#
#         embed.set_footer(text="Universium", icon_url=itx.guild.icon)
#         await itx.response.send_message(embed=embed, ephemeral=True)
#
#     @app_commands.command(name="cancel", description="Cancel an outgoing contract")
#     @app_commands.describe(contract_id="ID listed on the contract")
#     async def contract_delete(self, itx: discord.Interaction, contract_id: int):
#         DB = BankDB()
#         contracts = DB.list_contracts(itx.user.id)
#
#         for contract in contracts:
#             if contract[0] == contract_id:
#                 DB.delete_contract(contract_id)
#                 await itx.response.send_message(
#                     f"The Contract with ID {contract_id} between yourself and <@{contract[2]}> has been cancelled",
#                     ephemeral=True,
#                 )
#                 return
#         await itx.response.send_message(
#             f"You do not control a contract with ID {contract_id}.", ephemeral=True
#         )

class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #    @app_commands.command(name="tax", description="Set Tax Rate")
    #    @app_commands.checks.has_permissions(administrator=True)
    #    @app_commands.describe(tax="enter numeric tax rate between 0-100")
    #    async def set_taxrate(self, itx: discord.Interaction, tax: str):
    #        try:
    # Attempt to convert the value to a number (integer or float)
    #            float_value = float(tax)
    #        except ValueError:
    # If a ValueError occurs, the value cannot be converted to a number
    #            await itx.response.send_message("The tax rate could not be evaluated. Please enter a numeric value between 0-100", ephemeral=True)
    #            return
    #        DB = BankDB()
    #        float_value = float_value / 100
    #        DB.set_tax(float_value)
    #        await itx.response.send_message(f"The tax rate has been set to {tax}", ephemeral=True)

    #    @app_commands.command(name="bonus", description="Set Message Bonus Rate")
    #    @app_commands.checks.has_permissions(administrator=True)
    #    @app_commands.describe(bonus="enter numeric bonus rate between 0-100")
    #    async def set_bonusrate(self, itx: discord.Interaction, bonus: str):
    #        try:
    # Attempt to convert the value to a number (integer or float)
    #            float_value = float(bonus)
    #        except ValueError:
    #            # If a ValueError occurs, the value cannot be converted to a number
    #            await itx.response.send_message("The bonus rate could not be evaluated. Please enter a numeric value between 0-100", ephemeral=True)
    #            return
    #        DB = BankDB()
    #        float_value = float_value / 100
    #        DB.set_bonus(float_value)
    #        await itx.response.send_message(f"The bonus rate has been set to {bonus}", ephemeral=True)

    @app_commands.command(name="balance", description="Check your Equity balance")
    async def balance(self, itx: discord.Interaction):

        await itx.response.defer(ephemeral=True, thinking=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{apiLink}/balance",
                json={
                    "user_id": str(itx.user.id)
                }
            ) as resp:
                data = await resp.json()
                if resp.status == 200:
                    log.info(f"balance: {itx.user} {data['result']}")
                else:
                    log.warning(f"balance {resp.status}: {itx.user} {data}")
                    await itx.edit_original_response(content='Trouble fetching balance')
                    return

        embed = discord.Embed(
            title=f"{itx.user}'s Balance", description=f"*You have {data['result']} Equity*"
        )

        embed.set_thumbnail(
            url=itx.user.avatar.url if itx.user.avatar.url else itx.user.default_avatar
        )

        embed.set_footer(text=itx.guild.name, icon_url=itx.guild.icon)

        await itx.edit_original_response(embed=embed)

    @app_commands.command(name="pay", description="Give another user Equity")
    @app_commands.describe(hide="whether to hide the message or not (True by default)")
    async def pay(self, itx: discord.Interaction, user: discord.Member, amount: int, hide: bool = True):

        await itx.response.defer(ephemeral=hide, thinking=True)

        sender_id = str(itx.user.id)
        receiver_id = str(user.id)

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
                    log.info(f"pay: {amount} {itx.user} -> {user}")
                    await itx.edit_original_response(content=f"{'You' if hide else itx.user.mention} paid {user.mention} {amount} Equity",
                        allowed_mentions=discord.AllowedMentions(users=False))
                    return
                elif resp.status == 400:
                    log.warning(f"pay {resp.status}: {amount} {itx.user} -> {user} => {data['result']}")
                    await itx.edit_original_response(content=data['result'])
                    return
                else:
                    log.warning(f"pay {resp.status}: {amount} {itx.user} -> {user} => {data['result']}")
                    # await itx.response.send_message(f"You dont have {coins} coins to give to {user}.")
                    await itx.edit_original_response(content=f"Trouble sending Equity to {user}")
                    return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
    # await bot.add_cog(ContractGroup(bot))
    # await bot.add_cog(AdminContractGroup(bot))
