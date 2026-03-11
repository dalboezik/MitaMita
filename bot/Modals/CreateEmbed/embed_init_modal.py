#imports
import disnake
from bot_init import bot

class EmbedInitModal(disnake.ui.Modal):
    """
    A modal to initialize an embed:
    - Prompts the user to enter a title and a description for the embed.
    - Sends the embed to the temporary embed creation channel with buttons for further editing.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
    """
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
        """Creates a temporary channel and sends the initial embed."""
        #Channel creation ->
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

        #Sends the embed to the newly created channel ->
        await cahnnel.send(f"{inter.author.mention}, you can edit your embed in this channel.")
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
            f"Your embed can be edited in <#{channel.id}>.",
            ephemeral=True,
            delete_after=8
        )
