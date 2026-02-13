#imports
import disnake
from bot_init import bot
from disnake.ext import commands
from Modals.CreateEmbed.embed_init_modal import EmbedInitModal
from Modals.CreateEmbed.add_field_modal import AddFieldModal
from SelectMenus.CreateEmbed.remove_field_dropdown import RemoveFieldDropdown

class CreateEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="create_embed", description="---")
    async def create_embed(self, inter: disnake.CommandInteraction):
        await inter.response.send_modal(EmbedInitModal())


    @commands.Cog.listener("on_button_click")
    async def add_field(self, inter: disnake.MessageInteraction):
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
        if inter.component.custom_id == "remove_field_btn":
            if inter.author == inter.message.interaction_metadata.user:
                await inter.response.send_message(
                    "", 
                    components=[
                        disnake.ui.Container(
                            disnake.ui.TextDisplay("## Remove field"),
                            disnake.ui.ActionRow(
                                RemoveFieldDropdown(inter.message.embeds[0])
                            )
                        ) 
                    ], 
                    ephemeral=True
                )
            else:
                await inter.response.send_message(
                    "Du hast keine Berechtigungen, um die Fleder zu löschen.",
                    ephemeral=True,
                    delete_after=5
                )

    
def setup(bot: commands.Bot):
    bot.add_cog(CreateEmbed(bot))