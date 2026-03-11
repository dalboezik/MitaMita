#imports
import config

import disnake

from datetime import datetime
from disnake.ext import commands

from bot_init import bot


class TicketModal(disnake.ui.Modal):
    """
    A modal dialog for capturing ticket details.

    This modal is triggered when a user clicks 'Create Ticket'.
    It validates user input and forwards the request to the moderation team.

    Input Fields:
        - Title (TextInput): A brief summary of the issue.
        - Description (TextInput): A detailed explanation of the concern.

    Workflow:
        1. Receives user input.
        2. Creates a structured embed with metadata (author, timestamp, status).
        3. Sends the request with an interaction button ('Accept') to the 
        configured ticket request channel.
        4. Confirms the creation to the user via an ephemeral follow-up.
    """

    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Title",
                placeholder="A brief summary of the issue",
                max_length=100,
                custom_id="problem_title",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="A detailed explanation of the concern",
                max_length=1000,
                custom_id="problem_description",
                style=disnake.TextInputStyle.paragraph
            )
        ]

        super().__init__(title="Create a ticket", components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        """Creates and sends the ticket to the TICKET_REQUEST_CHANNEL"""
        await inter.response.defer(ephemeral=True)
        
        #Embed init
        #Embed: 
        #   New ticket
        #   Created by: <@author>
        #   Subject: <Title of the ticket>
        #   Description: <Description of the ticket>
        #   Status: <Status of the ticket (Open, In Progress, Closed)>
        #   <timestamp>
        embed = disnake.Embed(title="New Ticket", timestamp=datetime.now())
        embed.add_field(name="", value=f"**Created by:** {inter.author.mention}", inline=False)

        embed.add_field(
            name="", 
            value=f"**Subject:** {inter.text_values.get("problem_title")}", 
            inline=False
        )

        embed.add_field(
            name="", 
            value=f"**Description:** {inter.text_values.get("problem_description")}", 
            inline=False
        )

        embed.add_field(name="", value="**Status:** Open", inline=False)

        # Send the embed
        TICKET_REQUEST_CHANNEL = bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID)

        if not TICKET_REQUEST_CHANNEL == None:
            await TICKET_REQUEST_CHANNEL.send(embed=embed, components=[
                disnake.ui.Button(
                    label="Accept",
                    custom_id="accept_ticket",
                    style=disnake.ButtonStyle.green
                )
            ])

            await inter.followup.send("Your ticket has been successfully created.", delete_after=8)
        else:
            print("Couldn't find the channel with the id: 'TICKET_REQUEST_CHANNEL_ID'.")
            await inter.followup.send(
                "The ticket-request-channel could not be found." +
                "Please contact the admins to resolve this problem."
            )
