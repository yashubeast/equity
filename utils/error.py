from discord import Interaction
from discord.app_commands import AppCommandError
from discord.app_commands.errors import CheckFailure
from utils.logger import log

class NotAdmin(CheckFailure):pass

async def app_command_error_handler(itx: Interaction, error: AppCommandError):
    if isinstance(error, NotAdmin):
        await itx.response.send_message("> Equity Admins only command", ephemeral=True)
        log.warning(f"non-admin user {itx.user} tried to use /{itx.command.qualified_name}")
    else:
        raise error
