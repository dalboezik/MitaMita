#imports
import disnake

import config
import temp

from disnake.ext import commands

from bot_init import bot
from Modals.ticket_modal import TicketModal
from utils.delete_chat_history import delete_chat_history


class Ticket(commands.Cog):
    """
    Cog for managing the ticket system.

    This class controls the entire lifecycle of a ticket:
    - Initialization of the ticket creation embed in the support channel.
    - Processing ticket creations via modals.
    - Management of ticket requests in moderation channels.
    - Dynamic creation of private text channels for communication.
    - Closing and archiving tickets, including status updates.

    Attributes:
        bot (commands.Bot): Die Instanz des Discord-Bots.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def sendTicketEmbed():
        """Sends a ticket creation embed/container in the support channel"""

        #Embed ->
        '''
        embed = disnake.Embed(title="Create a ticket", description=config.TICKET_MESSAGE)

        await delete_chat_history(config.TICKET_CHANNEL_ID)

        await bot.get_channel(config.TICKET_CHANNEL_ID).send(embed=embed, components=[
            disnake.ui.Button(
                label="Create a ticket",
                custom_id="create_ticket",
                style=disnake.ButtonStyle.danger
            )
        ])
        '''

        # Container ->
        container = disnake.ui.Container(
            disnake.ui.TextDisplay(
                "## Create a ticket"
            ),
            disnake.ui.TextDisplay(
                f"{config.TICKET_MESSAGE}"
            ),
            disnake.ui.ActionRow(
                disnake.ui.Button(
                    label="Create a ticket",
                    custom_id="create_ticket",
                    style=disnake.ButtonStyle.danger
                )
            )
        )

        await delete_chat_history(config.TICKET_CHANNEL_ID)
        await bot.get_channel(config.TICKET_CHANNEL_ID).send(components=container)


    @commands.Cog.listener("on_button_click")
    async def create_ticket_embed(self, inter: disnake.MessageInteraction):
        """Creates a ticket and post it to the TICKET_REQUEST_CHANNEL"""
        if inter.component.custom_id == "create_ticket":
            await inter.response.send_modal(TicketModal())


    @commands.Cog.listener("on_button_click")
    async def accept_ticket(self, inter: disnake.MessageInteraction):
        """
        Creates a temorary channel with the moderator and the ticket author, 
        and updates the ticket status..
        """
        if inter.component.custom_id == "accept_ticket":
            await inter.response.defer(ephemeral=True)

            # Get the ticket author
            ticket_author: disnake.Member = inter.guild.get_member(int(
                inter.message.embeds[0].fields[0].value.split(":")[1][5:-1]
                )
            )

            # Creates a ticket category if it doesn't exist 
            if not disnake.utils.get(inter.guild.categories, name="tickets"):
                await inter.guild.create_category(name="tickets", position=1)

            # Creates a temp channel with the mod and the ticket author
            ticket_channel =  await inter.guild.create_text_channel(
                name=f"{ticket_author.global_name}-ticket", 
                category=disnake.utils.get(
                    inter.guild.categories, 
                    name="tickets"
                ),
                overwrites={
                    inter.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
                    inter.author: disnake.PermissionOverwrite(view_channel=True),
                    ticket_author: disnake.PermissionOverwrite(view_channel=True),
                    bot.user: disnake.PermissionOverwrite(view_channel=True)
                }
            )

            # Updates the status of the ticket in the TICKET_REQUEST_CHANNEL
            inter.message.embeds[0].set_field_at(
                index=-1,
                name="",
                value="**Status:** In Progress",
                inline=False
            )

            await inter.message.delete()
            ticket_embed= await inter.channel.send(embed=inter.message.embeds[0])

            #Saves the metadata of the ticket
            temp.ticket_context.update({
               ticket_channel.id: {
                    "ticket_embed": ticket_embed,
                    "ticket_author_id": ticket_author.id,
                    "ticket_mod_id": inter.author.id
                }
            })
            
            # Send a notification to the newly created channel
            # Embed: 
            #   Moderator <@Mod> has accepted your ticket:
            #   > Title: <Title of the ticket>
            #   > Description: <Description of the ticket>
            #   You can now discuss the issue here and work towards a resolution.
            embed = disnake.Embed()
            embed.add_field(
                name="", 
                value=f"**Moderator {inter.author.mention} has accepted your ticket:**", 
                inline=False
            )

            embed.add_field(name="", value=f"""> {inter.message.embeds[0].fields[1].value}
            > {inter.message.embeds[0].fields[2].value}""", inline=False)

            embed.add_field(
                name="", 
                value="You can now discuss the issue here and work towards a resolution.", 
                inline=False
            )

            await ticket_channel.send(ticket_author.mention)
            await ticket_channel.send(embed=embed)

        
    @commands.slash_command(
        name="close-ticket", 
        description="Closes the current ticket and archives its status."
    )
    async def close_ticket(self, inter: disnake.CommandInteraction):
        """Closes the current ticket and archives its status."""
        if inter.channel.category.name == config.TICKET_CATEGORY_NAME:
            await inter.channel.set_permissions(inter.author, view_channel=False)

            # Check if the moderator closed the ticket.
            isMod = False
            for role in inter.author.roles:
                if role.id == config.MOD_ROLE_ID:
                    isMod = True
                    break

            if isMod:
                await inter.response.send_message(f"{inter.author.mention} closed the ticket.\n"+
                "Was this consultation helpful?", components=[
                    disnake.ui.Button(
                        label="Yes",
                        custom_id="helpful_ticket",
                        style=disnake.ButtonStyle.green
                    ),
                    disnake.ui.Button(
                        label="No",
                        custom_id="unhelpful_ticket",
                        style=disnake.ButtonStyle.danger
                    )       
                ])
            else:
                #updtaes the ticket status to Closed
                await inter.response.send_message(f"{inter.author.mention} closed the ticket.")
                temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0].set_field_at(
                    index=-1,
                    name="",
                    value="**Status:** Closed",
                    inline=False
                )

                #deletes the metadata of the ticket from the temp
                await temp.ticket_context[inter.channel.id]["ticket_embed"].delete()

                #send the updated ticket
                if config.SHOW_COMPLETED_TICKETS:
                    await bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID).send(
                        embed=temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0])
                
            if len(inter.channel.members) == 2:
                temp.ticket_context.pop(inter.channel.id)
                await inter.channel.delete()

        else:
            await inter.response.send_message(
                "This command can only be used within ticket channels.", 
                ephemeral=True
            )


    @commands.Cog.listener("on_button_click")
    async def helpful_ticket(self, inter: disnake.MessageInteraction):
        """Sets the ticket status to 'Closed' and deletes the ticket channel."""
        if inter.component.custom_id == "helpful_ticket":
            await inter.response.defer(ephemeral=True)

            temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0].set_field_at(
                index=-1,
                name="",
                value="**Status:** Closed",
                inline=False
            )

            await temp.ticket_context[inter.channel.id]["ticket_embed"].delete()
            if config.SHOW_COMPLETED_TICKETS:
                await bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID).send(
                    embed=temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0])
            
            temp.ticket_context.pop(inter.channel.id)
            await inter.channel.delete()


    @commands.Cog.listener("on_button_click")
    async def unhelpful_ticket(self, inter: disnake.MessageInteraction):
        """Sets the ticket status to 'Open' and deletes the temporary ticket channel."""
        if inter.component.custom_id == "unhelpful_ticket":
            await inter.response.defer(ephemeral=True)

            temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0].set_field_at(
                index=-1,
                name="",
                value="**Status:** Open",
                inline=False
            )

            await temp.ticket_context[inter.channel.id]["ticket_embed"].delete()
            await bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID).send(
                embed=temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0],
                components=[
                    disnake.ui.Button(
                        label="Accept",
                        custom_id="accept_ticket",
                        style=disnake.ButtonStyle.green
                    )
                ])

            temp.ticket_context.pop(inter.channel.id)
            await inter.channel.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))
