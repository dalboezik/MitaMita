#imports
import disnake
import temp
from bot_init import bot
from disnake.ext import commands

class RenameModal(disnake.ui.Modal):
    """
    A modal-dialog that allows the user to rename the voice channel
    if he is the owner of it.
    """
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Updated name",
                custom_id=("rename_text_input"),
                style=disnake.TextInputStyle.short
            )
        ]

        super().__init__(title="Rename the channel", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.defer(ephemeral=True)
        # Checking if the user has permission to edit this channel.
        if temp.voice_channels[inter.author.voice.channel.id] == inter.author:
            await inter.author.voice.channel.edit(name=inter.text_values.get("rename_text_input"))
            await inter.followup.send(
                "The name of the voice channel has been successfully updated.", 
                ephemeral=True
            )
        else:
            await inter.followup.send(
                "You don't have the permissions to edit the voice channel.",
                ephemeral=True
            )
