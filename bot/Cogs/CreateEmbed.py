#imports
import asyncio
import disnake

import config

from disnake.ext import commands

from utils.delete_chat_history import delete_chat_history

from bot_init import bot
from Modals.CreateEmbed.embed_init_modal import EmbedInitModal
from Modals.CreateEmbed.add_field_modal import AddFieldModal
from SelectMenus.CreateEmbed.remove_field_dropdown import DropDownView
from SelectMenus.CreateEmbed import select_channel_dropdown


class CreateEmbed(commands.Cog):
    """
    A cog for interactively creating Discord embeds.

    This class provides a slash command to initiate the embed creation process,
    along with various button listeners to dynamically edit the embed 
    (adding/removing fields or deleting the message).

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
    """

    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    async def send_init_container():
        """Sends a message with a button to start the embed creation process."""
        channel = bot.get_channel(config.CREATEEMBED_CHANNLE_ID)
        container = disnake.ui.Container(
            disnake.ui.TextDisplay("## Create Embed"),
            disnake.ui.TextDisplay("Here you can create your custom embed."),
            disnake.ui.ActionRow(disnake.ui.Button(
                label="Create Embed",
                custom_id="create_embed_btn",
                style=disnake.ButtonStyle.green
            ))
        )

        await delete_chat_history(config.CREATEEMBED_CHANNLE_ID)
        await channel.send(components=[container])


    @commands.Cog.listener("on_button_click")
    async def create_embed(self, inter: disnake.MessageInteraction):
        """Sends a modal to initialize the embed."""
        if inter.component.custom_id == "create_embed_btn":
            await inter.response.send_modal(EmbedInitModal())


    @commands.Cog.listener("on_button_click")
    async def add_field(self, inter: disnake.MessageInteraction):
        """Opens a modal to add a new field to the embed."""
        if inter.component.custom_id == "add_field_btn":
            await inter.response.send_modal(AddFieldModal())


    @commands.Cog.listener("on_button_click")
    async def set_img(self, inter: disnake.MessageInteraction):
        """Waits for an image upload from the user and sets it as the embed's image."""
        def check(m):
            return m.author == inter.author and m.channel == inter.channel

        if inter.component.custom_id == "set_img":
            message: disnake.Message | None = None

            await inter.response.send_message("Upload an image to set as the embed's image.")

            try:
                message = await bot.wait_for(event="message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await inter.followup.send("Time's up!")

            inter.message.embeds[0].set_image(url=message.attachments[0].url)

            await inter.message.edit(embed=inter.message.embeds[0])
            await asyncio.sleep(0.2)
            await message.delete()

    
    @commands.Cog.listener("on_button_click")
    async def set_thumbnail(self, inter: disnake.MessageInteraction):
        """Waits for an image upload from the user and sets it as the embed's thumbnail."""
        def check(m):
            return m.author == inter.author and m.channel == inter.channel

        if inter.component.custom_id == "set_thumbnail":
            message: disnake.Message | None = None

            await inter.response.send_message("Upload an image to set as the embed's thumbnail.")

            try:
                message = await bot.wait_for(event="message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await inter.followup.send("Time's up!")

            inter.message.embeds[0].set_thumbnail(url=message.attachments[0].url)

            await inter.message.edit(embed=inter.message.embeds[0])
            await asyncio.sleep(0.2)
            await message.delete()


    @commands.Cog.listener("on_button_click")
    async def send_embed(self, inter: disnake.MessageInteraction):
        """Sends a dropdown to select a channel where the embed should be sent."""
        if inter.component.custom_id == "embed_done_btn":
            await inter.response.send_message(
                view=select_channel_dropdown.DropDownView(inter.message),
                ephemeral=True
            )


    @commands.Cog.listener("on_button_click")
    async def remove_field(self, inter: disnake.MessageInteraction):
        """Sends a dropdown that all fields which can be deleted."""
        if inter.component.custom_id == "remove_field_btn":
            await inter.response.send_message(
                "## Remove a field", 
                view=DropDownView(message=inter.message),
                ephemeral=True
            )


    @commands.Cog.listener("on_button_click")
    async def delete_channel(self, inter: disnake.MessageInteraction):
        """Deletes the temporary channel used for embed creation."""
        if inter.component.custom_id == "delete_channel":
            await inter.channel.delete()

    
def setup(bot: commands.Bot):
    bot.add_cog(CreateEmbed(bot))
