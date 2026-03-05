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
        cahnnel = await inter.guild.create_text_channel(
            name=inter.text_values.get("embed_title"),
            category=disnake.utils.get(
                inter.guild.categories,
                name="start"
            ),
            overwrites={
                inter.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
                inter.author: disnake.PermissionOverwrite(view_channel=True),
                bot.user: disnake.PermissionOverwrite(view_channel=True)
            }
        )

        await cahnnel.send(f"{inter.author.mention}, hier kannst du dein Embed bearbeiten")
        await cahnnel.send(
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
                    label="Set image",
                    custom_id="set_img",
                    style=disnake.ButtonStyle.blurple
                ),
                disnake.ui.Button(
                    label="Set thumbnail",
                    custom_id="set_thumbnail",
                    style=disnake.ButtonStyle.gray
                ),
                disnake.ui.Button(
                    label="Done",
                    custom_id="embed_done_btn",
                    style=disnake.ButtonStyle.green
                ),
                disnake.ui.Button(
                    label="Delete embed",
                    custom_id="delete_channel",
                    style=disnake.ButtonStyle.gray
                )
            ]
        )

        await inter.response.send_message(
            f"In dem Channel <#{cahnnel.id}> kannst du dein Embed bearbeiten.",
            ephemeral=True,
            delete_after=8
        )
