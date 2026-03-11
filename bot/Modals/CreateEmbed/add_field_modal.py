#imports
import disnake
from bot_init import bot

class AddFieldModal(disnake.ui.Modal):
    """
    A modal to add custom fields to the embed:
    - Prompts the user to enter a name, value, and the inline setting (True/False).
    - Appends the new field to the embed

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
    """
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Name",
                custom_id="field_name",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Value",
                custom_id="field_value",
                style=disnake.TextInputStyle.paragraph
            ),
            disnake.ui.TextInput(
                label="Inline",
                custom_id="field_inline",
                style=disnake.TextInputStyle.short,
                value="True"
            )
        ]

        super().__init__(title="Add field", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        """Appends the new field to the embed"""
        embed = inter.message.embeds[0].add_field(
            name=inter.text_values.get("field_name"),
            value=inter.text_values.get("field_value"),
            inline=eval(inter.text_values.get("field_inline").capitalize())
        )

        await inter.message.edit(
            embed=embed
        )

        await inter.response.send_message(
            "The new field has been successfully added to the embed.",
            ephemeral=True,
            delete_after=5
        )
