#imports
import disnake

import config

from disnake.ext import commands

from bot_init import bot


class Greeting(commands.Cog):
    """Greets the new members."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):

        FORMATED_GREETING_MESSAGE = config.GRETTING_MESSAGE.format(name=member.mention)
        
        # Embed ->
        embed = disnake.Embed(
            title=f"Wilkommen, {member.global_name}", 
            description=f"{FORMATED_GREETING_MESSAGE}"
        )
        embed.set_thumbnail(member.default_avatar.url)

        await bot.get_channel(config.GREETING_CHANNEL_ID).send(embed=embed)
        

def setup(bot: commands.Bot):
    bot.add_cog(Greeting(bot))
