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
    Ein Cog zur interaktiven Erstellung von Discord-Embeds.

    Diese Klasse bietet einen Slash-Command zum Initiieren eines Embed-Erstellungsprozesses
    sowie verschiedene Button-Listener, um den Embed dynamisch zu bearbeiten (Felder hinzufügen, 
    entfernen oder die Nachricht löschen).

    Attributes:
        bot (commands.Bot): Die Instanz des Discord-Bots.
    """

    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    async def send_init_container():
        channel = bot.get_channel(config.CREATEEMBED_CHANNLE_ID)
        container = disnake.ui.Container(
            disnake.ui.TextDisplay("## Create Embed"),
            disnake.ui.TextDisplay("Hier kannst du ein Embed erstellen"),
            disnake.ui.ActionRow(disnake.ui.Button(
                label="Create Embed",
                custom_id="create_embed_btn",
                style=disnake.ButtonStyle.green
            ))
        )

        await delete_chat_history(config.CREATEEMBED_CHANNLE_ID)
        await channel.send(components=[container])


    '''
    @commands.slash_command(name="create_embed", description="Erstellt einen Embed")
    async def create_embed(self, inter: disnake.CommandInteraction):
        """Sendet das initiale Modal zur Erstellung eines Embeds."""
        await inter.response.send_modal(EmbedInitModal())
    '''


    @commands.Cog.listener("on_button_click")
    async def create_embed(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "create_embed_btn":
            await inter.response.send_modal(EmbedInitModal())


    @commands.Cog.listener("on_button_click")
    async def add_field(self, inter: disnake.MessageInteraction):
        """Öffnet ein Modal zum Hinzufügen eines neuen Embed-Feldes."""
        if inter.component.custom_id == "add_field_btn":
            await inter.response.send_modal(AddFieldModal())


    @commands.Cog.listener("on_button_click")
    async def set_img(self, inter: disnake.MessageInteraction):
        def check(m):
            return m.author == inter.author and m.channel == inter.channel

        if inter.component.custom_id == "set_img":
            message: disnake.Message | None = None

            await inter.response.send_message("Lade in diesen Channel ein Bild hoch.")

            try:
                message = await bot.wait_for(event="message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await inter.followup.send("Das hat zu lange gedauert.")

            inter.message.embeds[0].set_image(url=message.attachments[0].url)

            await inter.message.edit(embed=inter.message.embeds[0])
            await asyncio.sleep(0.2)
            await message.delete()

    
    @commands.Cog.listener("on_button_click")
    async def set_thumnail(self, inter: disnake.MessageInteraction):
        def check(m):
            return m.author == inter.author and m.channel == inter.channel

        if inter.component.custom_id == "set_thumbnail":
            message: disnake.Message | None = None

            await inter.response.send_message("Lade in diesen Channel ein Bild hoch.")

            try:
                message = await bot.wait_for(event="message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await inter.followup.send("Das hat zu lange gedauert.")

            inter.message.embeds[0].set_thumbnail(url=message.attachments[0].url)

            await inter.message.edit(embed=inter.message.embeds[0])
            await asyncio.sleep(0.2)
            await message.delete()


    @commands.Cog.listener("on_button_click")
    async def delete_embed(self, inter: disnake.MessageInteraction):
        """
        Löscht das aktuelle Embed, das noch nicht fertiggestellt ist, 
        falls der inter.author der Author von dem Embed ist.
        """
        if inter.component.custom_id == "delete_embed_btn":
            await inter.message.delete()
            await inter.response.send_message(
                "Die Nachricht wurde erfolreich gelöscht.",
                ephemeral=True,
                delete_after=5
            )


    '''
    @commands.Cog.listener("on_button_click")
    async def send_embed(self, inter: disnake.MessageInteraction):
        """Stellt das Embed fertig"""
        if inter.component.custom_id == "embed_done_btn":
            if inter.author == inter.message.interaction_metadata.user:
                await inter.message.edit(components=[])
                await inter.response.send_message(
                    "Dein Embed ist fertig.", 
                    ephemeral=True, 
                    delete_after=5
                )
            else:
                await inter.response.send_message(
                    "Du hast keine Berechtigungen, um den Embed fertig zu stellen.",
                    ephemeral=True,
                    delete_after=5
                )
    '''


    @commands.Cog.listener("on_button_click")
    async def send_embed(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "embed_done_btn":
            await inter.response.send_message(
                view=select_channel_dropdown.DropDownView(inter.message),
                ephemeral=True
            )


    @commands.Cog.listener("on_button_click")
    async def remove_field(self, inter: disnake.MessageInteraction):
        """Sendet ein Dropdown mit allen Feldern, die man löschen kann."""
        if inter.component.custom_id == "remove_field_btn":
            await inter.response.send_message(
                "## Remove a field", 
                view=DropDownView(message=inter.message),
                ephemeral=True
            )


    @commands.Cog.listener("on_button_click")
    async def delete_channel(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "delete_channel":
            await inter.channel.delete()

    
def setup(bot: commands.Bot):
    bot.add_cog(CreateEmbed(bot))
