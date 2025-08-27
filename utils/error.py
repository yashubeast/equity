from discord import Interaction
from discord.errors import NotFound
from discord.app_commands import AppCommandError
from discord.app_commands.errors import CheckFailure
from utils.logger import log

class NotAdmin(CheckFailure):pass

async def app_command_error_handler(itx: Interaction, error: AppCommandError):
    if isinstance(error, NotAdmin):
        await itx.response.send_message("> Equity Admins only command", ephemeral=True)
        log.warning(f"non-admin user {itx.user} tried to use /{itx.command.qualified_name}")
    
    if isinstance(error, NotFound) and "Unknown interaction" in str(error):
        log.warning(f"expired interaction command '{itx.command.name}' from user {itx.user.id} expired before response")
        return

    raise error