# imports
import config
import disnake
from bot_init import bot
from disnake.ext import commands
from datetime import datetime

#TODO: Status von den Reporten hinzufügen

class Report(commands.Cog):
    def __init__(self, bot: disnake.Bot):
        self.bot = bot

    @commands.slash_command(name="report", description="------")
    async def report(self, inter: disnake.CommandInteraction, member: disnake.Member, reason: str):
        await inter.response.defer(ephemeral=True)
        
        embed = disnake.Embed(
            title="Neuer Report", 
            description=f"- 👤 **Von:** {inter.author.mention}\n" +
            f"- 🚫 **Gegen:** {member.mention}\n" +
            f"- 📍 **Kanal:** {inter.channel.mention}",
            timestamp=datetime.now()
        )
        embed.add_field(
            name="Details:", 
            value=f"- 📝 **Grund:** {reason}", #f"- 📝 **Grund:** {reason}\n- ⏰ **Zeitpunkt:** {datetime.now()}",
            inline=False
        )

        if not config.REPORT_CHANNEL_ID == None:
            await bot.get_channel(config.REPORT_CHANNEL_ID).send(embed=embed)
            
            await inter.followup.send(
                content="Dein Report wurde erfolgreich erstellt.\n" +
                "Die Mods werden sol schnell wie möglich eingreifen.",
                delete_after=8
            )
        else:
            print("Der Channel mit der ID: 'REPORT_CHANNEL_ID' konnte nicht gefunden werden.")
            await inter.followup.send(
                content="Der Channel mit den Report-Anfragen konnte nicht gefunden werden," + 
                "bitte kontaktiere die Admins, um das Problem zu beheben."
            )

def setup(bot: disnake.Bot):
    bot.add_cog(Report(bot))