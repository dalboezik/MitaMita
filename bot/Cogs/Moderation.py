# imports
import disnake
from bot_init import bot
from disnake.ext import commands
from Modals.Moderation.kick_modal import KickModal
from Modals.Moderation.ban_modal import BanModal
from Modals.Moderation.timeout_modal import TimeoutModal

class Moderation(commands.Cog):
    """
    Ein Cog zur Verwaltung von Moderations-Befehlen.
    
    Diese Klasse stellt Slash-Commands bereit, die interaktive Modals öffnen,
    um Nutzer zu kicken, zu bannen oder stummzuschalten (Timeout).
    """

    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(
        name="kick", 
        description="Kickt den angegebenen User nach Angabe eines Grundes"
    )
    async def kick(self, inter: disnake.CommandInteraction, member: disnake.Member):
        """Öffnet ein Modal, um ein Mitglied vom Server zu kicken."""
        await inter.response.send_modal(KickModal(member=member))

    @commands.slash_command(
        name="ban", 
        description="Bannt den angegebenen User nach Angabe eines Grundes"
    )
    async def ban(self, inter: disnake.CommandInteraction, member: disnake.Member):
        """Öffnet ein Modal, um ein Mitglied dauerhaft vom Server zu bannen."""
        await inter.response.send_modal(BanModal(member=member))

    @commands.slash_command(name="timeout", description="Schickt den ausgewählten User in ein Timeout")
    async def timeout(self, inter: disnake.CommandInteraction, member: disnake.Member):
        """Öffnet ein Modal, um ein Mitglied für einen bestimmten Zeitraum stummzuschalten."""
        await inter.response.send_modal(TimeoutModal(member=member))


    # Errorhandling ------------->
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(
                "Das Mitglied wurde nicht gefunden",
                ephemeral=True,
                delete_after=5
            )

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send(
                "Das Mitglied wurde nicht gefunden",
                ephemeral=True,
                delete_after=5
            )


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
