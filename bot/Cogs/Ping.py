# imports
import disnake

from disnake.ext import commands

from bot_init import bot


class Ping(commands.Cog):
    """
    Allows to ping the bot to check the connection.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Ping the bot")
    async def ping(self, inter: disnake.CommandInteraction):
        await inter.response.send_message(
            f"{bot.user} answered in {bot.latency}ms.", 
            ephemeral=True
        )

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))