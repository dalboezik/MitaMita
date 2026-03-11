#imports
import disnake
import temp
from bot_init import bot
from disnake.ext import commands

class SetLimitModal(disnake.ui.Modal):
    """
    A modal-dialog that allows the user to set and update 
    the user limit of the voice channel.
    """
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Set limit",
                custom_id="limit_text_input",
                style=disnake.TextInputStyle.short,
            )
        ]

        super().__init__(title="Update user limit", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        # Checking if the user has permission to edit this channel.
        if temp.voice_channels[inter.author.voice.channel.id] == inter.author:
            try:
                await inter.author.voice.channel.edit(
                    user_limit=int(inter.text_values.get("limit_text_input"))
                )
                await inter.response.send_message(
                    "The user limit of the channel has been successfully updated.", 
                    ephemeral=True
                )
                
            except ValueError as error:
                await inter.response.send_message(
                    "Only integers are allowed as input.",
                    ephemeral=True
                )

            except disnake.errors.HTTPException as error:
                await inter.response.send_message(
                    "Only integers are allowed as input.", 
                    ephemeral=True
                )
        else:
            await inter.response.send_message(
                "You don't have the permissions to edit the voice channel.",
                ephemeral=True
            )
