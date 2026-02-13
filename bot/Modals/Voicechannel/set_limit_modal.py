#imports
import disnake
import temp
from bot_init import bot
from disnake.ext import commands

class SetLimitModal(disnake.ui.Modal):
    """
    Ein Modal-Dialog, der es Benutzern ermöglicht, das Teilnehmerlimit 
    ihres aktuellen Sprachkanals über ein Textfeld zu ändern.
    """
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Limit ändern",
                custom_id="limit_text_input",
                style=disnake.TextInputStyle.short,
            )
        ]

        super().__init__(title="Limit ändern", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        # Prüfen, ob der inter.author den Channel ändern darf
        if temp.voice_channels[inter.author.voice.channel.id] == inter.author:
            try:
                await inter.author.voice.channel.edit(
                    user_limit=int(inter.text_values.get("limit_text_input"))
                )
                await inter.response.send_message("Das Limit wurde erfolgreich geändert.", ephemeral=True)
                
            except ValueError as error:
                await inter.response.send_message(
                    "In der Eingabe Werden nur Ganzzahlen erwartet.",
                    ephemeral=True
                )

            except disnake.errors.HTTPException as error:
                await inter.response.send_message(
                    "In der Eingabe Werden nur Ganzzahlen erwartet.", 
                    ephemeral=True
                )
        else:
            await inter.response.send_message(
                "Du hast keine Berechtigungen, um den Channel zu bearbeiten.",
                ephemeral=True
            )
