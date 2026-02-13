#imports
import config
import disnake
from bot_init import bot
from datetime import datetime
from disnake.ext import commands

class TicketModal(disnake.ui.Modal):
    """
    Ein modales Dialogfenster zur Erfassung von Ticket-Details.

    Dieses Modal wird aufgerufen, wenn ein Benutzer auf 'Ticket erstellen' klickt.
    Es validiert die Benutzereingaben und leitet die Anfrage an das Moderationsteam weiter.

    Eingabefelder:
        - Titel (TextInput): Kurze Zusammenfassung des Problems.
        - Beschreibung (TextInput): Detaillierte Erläuterung des Anliegens.

    Workflow:
        1. Nimmt Benutzereingaben entgegen.
        2. Erstellt ein strukturiertes Embed mit Metadaten (Author, Zeitstempel, Status).
        3. Sendet die Anfrage mit einem Interaktions-Button ('Annehmen') in den 
           konfigurierten Ticket-Request-Kanal.
        4. Bestätigt dem Benutzer die Erstellung via ephemeral Follow-up.
    """

    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Titel",
                placeholder="Nenne dein Problem",
                max_length=100,
                custom_id="problem_title",
                style=disnake.TextInputStyle.short
            ),
            disnake.ui.TextInput(
                label="Beschreibung",
                placeholder="Beschreibe dein Problem",
                max_length=1000,
                custom_id="problem_description",
                style=disnake.TextInputStyle.paragraph
            )
        ]

        super().__init__(title="Ticket erstellen", components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        """Erstellt einen neuen Ticket und schickt den in den TICKET_REQUEST_CHANNEL"""
        await inter.response.defer(ephemeral=True)
        
        #Initialisierung des Embeds
        #Embed: 
        #   Neue Ticketanfrage
        #   Erstellt von: <@author>
        #   Thema: <Thema von dem Ticket>
        #   Beschreibung: <Beschreibung von dem Ticket>
        #   Status: <Status von dem Ticket (Offen, In Besprechung, Erledigt)>
        #   <timestamp>
        embed = disnake.Embed(title="Neue Ticketanfrage", timestamp=datetime.now())
        embed.add_field(name="", value=f"**Erstellt von:** {inter.author.mention}", inline=False)

        embed.add_field(
            name="", 
            value=f"**Thema:** {inter.text_values.get("problem_title")}", 
            inline=False
        )

        embed.add_field(
            name="", 
            value=f"**Beschreibung:** {inter.text_values.get("problem_description")}", 
            inline=False
        )

        embed.add_field(name="", value="**Status:** Offen", inline=False)

        # Abschicken des Embeds
        TICKET_REQUEST_CHANNEL = bot.get_channel(config.TICKET_REQUEST_CHANNEL_ID)

        if not TICKET_REQUEST_CHANNEL == None:
            await TICKET_REQUEST_CHANNEL.send(embed=embed, components=[
                disnake.ui.Button(
                    label="Annehmen",
                    custom_id="accept_ticket",
                    style=disnake.ButtonStyle.green
                )
            ])

            await inter.followup.send("Dein Ticket wurde erfolgreich erstellt.", delete_after=8)
        else:
            print("Der Channel mit der ID:'TICKET_REQUEST_CHANNEL_ID' konnte nicht gefunden werden")
            await inter.followup.send(
                "Der Ticket-Anfrage-Chnannel konnte nicht gefunden werden," +
                "bitte kontaktiere die Admins, um das Problem zu beheben."
            )
