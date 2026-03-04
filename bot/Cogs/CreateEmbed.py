#imports
import disnake

from disnake.ext import commands

from bot_init import bot
from Modals.CreateEmbed.embed_init_modal import EmbedInitModal
from Modals.CreateEmbed.add_field_modal import AddFieldModal
from SelectMenus.CreateEmbed.remove_field_dropdown import DropDownView

#!Es besteht keine Möglichkeit ein Bild oder ein Thumnail zu setzen!

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


    @commands.slash_command(name="create_embed", description="Erstellt einen Embed")
    async def create_embed(self, inter: disnake.CommandInteraction):
        """Sendet das initiale Modal zur Erstellung eines Embeds."""
        await inter.response.send_modal(EmbedInitModal())


    @commands.Cog.listener("on_button_click")
    async def add_field(self, inter: disnake.MessageInteraction):
        """Öffnet ein Modal zum Hinzufügen eines neuen Embed-Feldes."""
        if inter.component.custom_id == "add_field_btn":
            if inter.author == inter.message.interaction_metadata.user:
                await inter.response.send_modal(AddFieldModal())
            else:
                await inter.response.send_message(
                    "Du hast keine Berechtigungen, um den Embed zu bearbeiten.",
                    ephemeral=True,
                    delete_after=5
                )


    @commands.Cog.listener("on_button_click")
    async def delete_embed(self, inter: disnake.MessageInteraction):
        """
        Löscht das aktuelle Embed, das noch nicht fertiggestellt ist, 
        falls der inter.author der Author von dem Embed ist.
        """
        if inter.component.custom_id == "delete_embed_btn":
            if inter.author == inter.message.interaction_metadata.user:
                await inter.message.delete()
                await inter.response.send_message(
                    "Die Nachricht wurde erfolreich gelöscht.",
                    ephemeral=True,
                    delete_after=5
                )
            else:
                await inter.response.send_message(
                    "Du hast keine Berechtigungen, um die Nachricht zu löschen.",
                    ephemeral=True,
                    delete_after=5
                )


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


    @commands.Cog.listener("on_button_click")
    async def remove_field(self, inter: disnake.MessageInteraction):
        """Sendet ein Dropdown mit allen Feldern, die man löschen kann."""
        if inter.component.custom_id == "remove_field_btn":
            if inter.author == inter.message.interaction_metadata.user:
                await inter.response.send_message(
                    "## Remove a field", 
                    view=DropDownView(message=inter.message),
                    ephemeral=True
                )
            else:
                await inter.response.send_message(
                    "Du hast keine Berechtigungen, um die Felder zu löschen.",
                    ephemeral=True,
                    delete_after=5
                )

    
def setup(bot: commands.Bot):
    bot.add_cog(CreateEmbed(bot))
