#imports
import disnake
import temp
from bot_init import bot
from disnake.ext import commands

class RenameModal(disnake.ui.Modal):
    """
    Ein Modal-Dialog, der es Benutzern ermöglicht, den Namen
    ihres aktuellen Sprachkanals über ein Textfeld zu ändern.
    """
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Neuer Name",
                custom_id=("rename_text_input"),
                style=disnake.TextInputStyle.short
            )
        ]

        super().__init__(title="Channel unbenennen", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.defer(ephemeral=True)
        # Prüfen, ob der inter.author den Channel ändern darf
        if temp.voice_channels[inter.author.voice.channel.id] == inter.author:
            await inter.author.voice.channel.edit(name=inter.text_values.get("rename_text_input"))
            await inter.followup.send(
                "Der Name von dem Voicechannel wurde erfolgreich geändert.", 
                ephemeral=True
            )
        else:
            await inter.followup.send(
                "Du hast keine Berechtigungen, um den Channel zu bearbeiten.",
                ephemeral=True
            )
