# imports
import disnake

from disnake.ext import commands

from bot_init import bot
from Modals.Moderation.kick_modal import KickModal
from Modals.Moderation.ban_modal import BanModal
from Modals.Moderation.timeout_modal import TimeoutModal

class Moderation(commands.Cog):
    """
    A Cog for managing moderation commands.

    This class provides slash commands that trigger interactive modals to 
    kick, ban, or timeout members.
    """

    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(
        name="kick", 
        description="Kicks the selected member after entering the reason."
    )
    async def kick(self, inter: disnake.CommandInteraction, member: disnake.Member):
        """Opens a modal to kick the selected member."""
        await inter.response.send_modal(KickModal(member=member))

    @commands.slash_command(
        name="ban", 
        description="Bans the selected member after entering the reason."
    )
    async def ban(self, inter: disnake.CommandInteraction, member: disnake.Member):
        """Opens a modal to ban the selected member."""
        await inter.response.send_modal(BanModal(member=member))

    @commands.slash_command(name="timeout", description="Schickt den ausgewählten User in ein Timeout")
    async def timeout(self, inter: disnake.CommandInteraction, member: disnake.Member):
        """Opens a modal to timeout a member."""
        await inter.response.send_modal(TimeoutModal(member=member))


    # Errorhandling ------------->
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(
                "The selected member couldn't be found.",
                ephemeral=True,
                delete_after=5
            )

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(
                "The selected member couldn't be found",
                ephemeral=True,
                delete_after=5
            )


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
