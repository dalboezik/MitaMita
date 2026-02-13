# imports
import config
import disnake
import temp
from bot_init import bot
from disnake.ext import commands
from Modals.Voicechannel.rename_modal import RenameModal
from Modals.Voicechannel.set_limit_modal import SetLimitModal

class VoiceChannel(commands.Cog):
    """
    Ein Cog zur dynamischen Verwaltung von Voice-Channels (Temp-Channels).
    
    Diese Klasse ermöglicht es Benutzern, temporäre Voice-Channels zu erstellen, 
    indem sie einem bestimmten 'Join-to-Create'-Channel beitreten. Sie bietet 
    Funktionen zum automatischen Löschen leerer Channels, zur Übergabe der 
    Channel-Inhaberschaft und zur Bearbeitung von Channel-Eigenschaften via 
    Modals oder Slash-Commands.

    Attribute:
        bot (commands.Bot): Die Instanz des Discord-Bots.
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(
        self, 
        member: disnake.Member, 
        before: disnake.VoiceState, 
        after: disnake.VoiceState
    ):
        """
        Überfällt Voice-Status-Updates, um:
        1. Neue temporäre Channels zu erstellen, wenn der 'Join-to-Create' Channel betreten wird.
        2. Leere temporäre Channels zu löschen.
        3. Die Inhaberschaft des Channels zu übertragen, wenn der Ersteller den Channel verlässt.
        """

        if before.channel != None and before.channel != after.channel:
            if before.channel.id != config.VOICE_CHANNEL_ID:
                if len(before.channel.members) == 0:
                    # Leeren Voicechannel löschen
                    temp.voice_channels.pop(before.channel.id)
                    await before.channel.delete()
                elif member == member.guild.get_member(temp.voice_channels[before.channel.id].id):
                    # Die Inhaberschaft des Channels übertragen, wenn der Inhaber nicht mehr in dem Channel ist
                    #print("Der Ersteller ist disconnected")
                    temp.voice_channels[before.channel.id] = before.channel.members[0]
            return   

        # Einen neuen Voice Channel erstellen
        if after.channel.id == config.VOICE_CHANNEL_ID:
            newVoiceChannel = await member.guild.create_voice_channel(
                name=f"{member.global_name}'s Voice Channel",
                category=disnake.utils.get(
                    member.guild.categories, 
                    id=config.VOICE_CHANNEL_CATEGORY_ID
                )
            )

            temp.voice_channels.update({newVoiceChannel.id: member})
            await member.move_to(newVoiceChannel)

            # Embed ->
            '''
            await newVoiceChannel.send(
                embed=disnake.Embed(title="Manage den Voicechannel"), 
                components=[
                    disnake.ui.Button(
                        label="Rename",
                        custom_id="rename_btn",
                    ),
                    disnake.ui.Button(
                        label="Set Limit",
                        custom_id="set_limit_btn"
                    )
                ]
            )
            '''
            
            # Container ->
            container = disnake.ui.Container(
                disnake.ui.TextDisplay(
                    "### Manage den Voicechannel"
                ),
                disnake.ui.ActionRow(
                    disnake.ui.Button(
                        label="Rename",
                        custom_id="rename_btn",
                        style=disnake.ButtonStyle.green
                    ),
                    disnake.ui.Button(
                        label="Set Limit",
                        custom_id="set_limit_btn",
                        style=disnake.ButtonStyle.blurple
                    )
                )
            )

            await newVoiceChannel.send(components=[container])


    # Modals, um den Channel zu managen
    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        """
        Verarbeitet Interaktionen mit den Kontroll-Buttons im Voice-Channel, um den Channel 
        zu verwalten.
        Öffnet entsprechende Modals.
        """

        if inter.component.custom_id == "rename_btn":
            await inter.response.send_modal(RenameModal())
        elif inter.component.custom_id == "set_limit_btn":
            await inter.response.send_modal(SetLimitModal())
            

    # Command, um den Channel zu managen
    @commands.slash_command(
        name="voice_channel", 
        description="Command zur manuellen Verwaltung des eigenen Voice-Channels."
    )
    async def voice_channel(self, inter: disnake.CommandInteraction, option: str, argument: str):
        """
        Slash-Command zur manuellen Verwaltung des eigenen Voice-Channels.

        Args:
            option (str): Die zu ändernde Eigenschaft (rename, set_limit).
            argument (str): Der neue Wert für die gewählte Option
        """

        await inter.response.defer(ephemeral=True)

        # Prüfen, ob der inter.author in einem Voicechannel ist
        if inter.author.voice == None:
            await inter.followup.send("Du bist aktuell in keinem Voicechannel drin.")
            return

        # Prüfen, ob der inter.author den Voicechannel bearbeiten darf
        if not temp.voice_channels[inter.author.voice.channel.id] == inter.author:
            await inter.followup.send(
                content="Du hast keine Berechtigungen, um den Channel zu bearbeiten.",
                ephemeral=True
            )
            return

        # Optionen
        if option == "rename":
            await inter.author.voice.channel.edit(name=argument)
            await inter.followup.send(
                content="Der Name von dem Voicechannel wurde erfolgreich geändert.", 
                ephemeral=True
            )
        elif option == "set_limit":
            await inter.author.voice.channel.edit(user_limit=int(argument))
            await inter.followup.send("Das Limit wurde erfolgreich geändert.", ephemeral=True)
        else:
            await inter.followup.send(f"'{option}': Unbekannte Option.")


    @voice_channel.autocomplete("option")
    async def option_autocomplete(self, inter: disnake.CommandInteraction, user_input: str):
        options = ["rename", "set_limit"]

        #[ausdruck for element in iterable if bedingung]
        #Returnt die options, die mit dem Input übereinstimmen
        return [option for option in options if user_input.lower() in option.lower()][:25]


    @voice_channel.error
    async def voice_channel_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Das argument erwartet eine ganze Zahl.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(VoiceChannel(bot))
