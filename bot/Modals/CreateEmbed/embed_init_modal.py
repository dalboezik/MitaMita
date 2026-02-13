#imports
import disnake
from bot_init import bot

class EmbedInitModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Title",
                custom_id="embed_title",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Description",
                custom_id="embed_description",
                style=disnake.TextInputStyle.paragraph
            )
        ]

        super().__init__(title="Create Embed", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.response.send_message(
            embed=disnake.Embed(
                title=inter.text_values.get("embed_title"),
                description=inter.text_values.get("embed_description")
            ),
            components=[
                disnake.ui.Button(
                    label="Add field",
                    custom_id="add_field_btn",
                    style=disnake.ButtonStyle.blurple
                ),
                disnake.ui.Button(
                    label="Remove field",
                    custom_id="remove_field_btn",
                    style=disnake.ButtonStyle.danger
                ),
                disnake.ui.Button(
                    label="Done",
                    custom_id="embed_done_btn",
                    style=disnake.ButtonStyle.green
                ),
                disnake.ui.Button(
                    label="Delete embed",
                    custom_id="delete_embed_btn",
                    style=disnake.ButtonStyle.gray
                )
            ],
            ephemeral=False
        )