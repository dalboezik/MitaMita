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
    Cog zur Verwaltung des Ticket-Systems.

    Diese Klasse steuert den gesamten Lebenszyklus eines Tickets:
    - Initialisierung des Ticket-Embeds im Support-Kanal.
    - Verarbeitung von Ticket-Erstellungen via Modals.
    - Management von Ticket-Anfragen in Moderations-Kanälen.
    - Dynamische Erstellung privater Text-Kanäle für die Kommunikation.
    - Abschluss und Archivierung von Tickets inklusive Status-Updates.

    Attributes:
        bot (commands.Bot): Die Instanz des Discord-Bots.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def sendTicketEmbed():
        """Sendet den Ticket-Embed/Container in den Support-Kanal"""

        #Embed ->
        '''
        embed = disnake.Embed(title="Ticket erstellen", description=config.TICKET_MESSAGE)

        await delete_chat_history(config.TICKET_CHANNEL_ID)

        await bot.get_channel(config.TICKET_CHANNEL_ID).send(embed=embed, components=[
            disnake.ui.Button(
                label="Ticket erstellen",
                custom_id="create_ticket",
                style=disnake.ButtonStyle.danger
            )
        ])
        '''

        # Container ->
        container = disnake.ui.Container(
            disnake.ui.TextDisplay(
                "## Ticket erstellen"
            ),
            disnake.ui.TextDisplay(
                f"{config.TICKET_MESSAGE}"
            ),
            disnake.ui.ActionRow(
                disnake.ui.Button(
                    label="Ticket erstellen",
                    custom_id="create_ticket",
                    style=disnake.ButtonStyle.danger
                )
            )
        )

        await delete_chat_history(config.TICKET_CHANNEL_ID)
        await bot.get_channel(config.TICKET_CHANNEL_ID).send(components=container)


    @commands.Cog.listener("on_button_click")
    async def create_ticket_embed(self, inter: disnake.MessageInteraction):
        """Erstellt einen neuen Ticket und schickt den in den TICKET_REQUEST_CHANNEL"""
        if inter.component.custom_id == "create_ticket":
            await inter.response.send_modal(TicketModal())


    @commands.Cog.listener("on_button_click")
    async def accept_ticket(self, inter: disnake.MessageInteraction):
        """
        Erstellt einen neuen Channel mit dem Mod und dem Ticketauthor 
        und ändert den Ticketstatus.
        """
        if inter.component.custom_id == "accept_ticket":
            await inter.response.defer(ephemeral=True)

            # Den Author von dem Ticket als Member bekommen
            ticket_author: disnake.Member = inter.guild.get_member(int(
                inter.message.embeds[0].fields[0].value.split(":")[1][5:-1]
                )
            )

            # tickets-Kategorie erstellen, falls nicht vorhanden 
            if not disnake.utils.get(inter.guild.categories, name="tickets"):
                await inter.guild.create_category(name="tickets", position=1)

            # Den ticket-channel mit dem Author und dem Mod erstellen
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

            # Den Status von dem Ticket aktualisieren
            inter.message.embeds[0].set_field_at(
                index=-1,
                name="",
                value="**Status:** In Besprechnung",
                inline=False
            )

            await inter.message.delete()
            ticket_embed= await inter.channel.send(embed=inter.message.embeds[0])

            # Die Metadaten von dem Ticket temporär abspeichern
            temp.ticket_context.update({
               ticket_channel.id: {
                    "ticket_embed": ticket_embed,
                    "ticket_author_id": ticket_author.id,
                    "ticket_mod_id": inter.author.id
                }
            })
            
            # Eine Benachrichtigung in den erstellten channel senden
            # Embed: 
            #   Der Mod <@Mod> hat Dein Ticket angenommen:
            #   > Titel: <Titel von dem Ticket>
            #   > Beschreibung: <Beschreibung von dem Ticket>
            #   Hier könnt ihr über das Problem sprechen und zu einer Lösung kommen.
            embed = disnake.Embed()
            embed.add_field(
                name="", 
                value=f"**Der Mod {inter.author.mention} hat Dein Ticket angenommen:**", 
                inline=False
            )

            embed.add_field(name="", value=f"""> {inter.message.embeds[0].fields[1].value}
            > {inter.message.embeds[0].fields[2].value}""", inline=False)

            embed.add_field(
                name="", 
                value="Hier könnt ihr über das Problem sprechen und zu einer Lösung konmmen.", 
                inline=False
            )

            await ticket_channel.send(ticket_author.mention)
            await ticket_channel.send(embed=embed)
            #print(f"Anzahl der Mitglieder: {inter.channel.members}")

        
    @commands.slash_command(
        name="close-ticket", 
        description="Schließt das aktuelle Ticket und archiviert den Status."
    )
    async def close_ticket(self, inter: disnake.CommandInteraction):
        """Schließt den Ticket und ändert den Status von dem Ticket"""
        if inter.channel.category.name == config.TICKET_CATEGORY_NAME:
            await inter.channel.set_permissions(inter.author, view_channel=False)

            # Prüfen, ob der Mod den Ticket geschlossen hat
            isMod = False
            for role in inter.author.roles:
                if role.id == config.MOD_ROLE_ID:
                    isMod = True
                    break

            if isMod:
                await inter.response.send_message(f"{inter.author.mention} hat den Ticket gechlossen.\n"+
                "War die Besprechnung hilfreich?", components=[
                    disnake.ui.Button(
                        label="Ja",
                        custom_id="helpful_ticket",
                        style=disnake.ButtonStyle.green
                    ),
                    disnake.ui.Button(
                        label="Nein",
                        custom_id="unhelpful_ticket",
                        style=disnake.ButtonStyle.danger
                    )       
                ])
            else:
                #ändert den Ticketstatus auf "Erledigt"
                await inter.response.send_message(f"{inter.author.mention} hat den Ticket geschlossen.")
                temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0].set_field_at(
                    index=-1,
                    name="",
                    value="**Status:** Erledigt",
                    inline=False
                )

                await temp.ticket_context[inter.channel.id]["ticket_embed"].delete()

                if config.SHOW_COMPLETED_TICKETS:
                    await bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID).send(
                        embed=temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0])
                
            if len(inter.channel.members) == 2:
                temp.ticket_context.pop(inter.channel.id)
                await inter.channel.delete()

            #print(f"Anzahl der Mitglieder: {len(inter.channel.members)}")
        else:
            await inter.response.send_message(
                "Die Command kann nur in den Tickets benutzt werden.", 
                ephemeral=True
            )


    @commands.Cog.listener("on_button_click")
    async def helpful_ticket(self, inter: disnake.MessageInteraction):
        """Stellt den Status von dem Ticket auf 'Erledigt' und löscht den Ticket Channel"""
        if inter.component.custom_id == "helpful_ticket":
            await inter.response.defer(ephemeral=True)

            temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0].set_field_at(
                index=-1,
                name="",
                value="**Status:** Erledigt",
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
        """Stellt den Status von dem Ticket auf 'Offen' und löscht den Ticket Channel"""
        if inter.component.custom_id == "unhelpful_ticket":
            await inter.response.defer(ephemeral=True)

            temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0].set_field_at(
                index=-1,
                name="",
                value="**Status:** Offen",
                inline=False
            )

            await temp.ticket_context[inter.channel.id]["ticket_embed"].delete()
            await bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID).send(
                embed=temp.ticket_context[inter.channel.id]["ticket_embed"].embeds[0],
                components=[
                    disnake.ui.Button(
                        label="Annehmen",
                        custom_id="accept_ticket",
                        style=disnake.ButtonStyle.green
                    )
                ])

            temp.ticket_context.pop(inter.channel.id)
            await inter.channel.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))
