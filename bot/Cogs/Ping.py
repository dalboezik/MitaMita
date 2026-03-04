# imports
import disnake

from disnake.ext import commands

from bot_init import bot


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="---")
    async def ping(self, inter: disnake.CommandInteraction):
        await inter.response.send_message(f"{bot.user} hat in {bot.latency}ms geantwortet", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))