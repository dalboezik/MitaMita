# imports
import disnake

import config

from datetime import datetime
from disnake.ext import commands

from bot_init import bot


#TODO: Status von den Reporten hinzufügen

class Report(commands.Cog):
    def __init__(self, bot: disnake.Bot):
        self.bot = bot

    @commands.slash_command(name="report", description="------")
    async def report(self, inter: disnake.CommandInteraction, member: disnake.Member, reason: str):
        await inter.response.defer(ephemeral=True)
        
        embed = disnake.Embed(
            title="New report", 
            description=f"- 👤 **From:** {inter.author.mention}\n" +
            f"- 🚫 **Against:** {member.mention}\n" +
            f"- 📍 **Channel:** {inter.channel.mention}",
            timestamp=datetime.now()
        )
        embed.add_field(
            name="Details:", 
            value=f"- 📝 **Reason:** {reason}",
            inline=False
        )

        if not config.REPORT_CHANNEL_ID == None:
            await bot.get_channel(config.REPORT_CHANNEL_ID).send(embed=embed)
            
            await inter.followup.send(
                content="Your report has been successfully submitted.\n" +
                "The moderators will take action as soon as possible.",
                delete_after=8
            )
        else:
            print("The channel with the ID 'REPORT_CHANNEL_ID' could not be found.")
            await inter.followup.send(
                content="The report channel could not be found.\n" + 
                "Please contact an administrator to resolve this issue."
            )


def setup(bot: disnake.Bot):
    bot.add_cog(Report(bot))