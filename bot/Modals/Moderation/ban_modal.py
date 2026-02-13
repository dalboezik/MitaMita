# imports
import disnake
from bot_init import bot

class BanModal(disnake.ui.Modal):
    """
    Ein interaktives Modal-Fenster zur Bestätigung eines Bans.
    
    Dieses Modal fragt den Moderator nach einem Grund für den Ban,
    informiert den betroffenen Nutzer per Privatnachricht und
    führt anschließend die Sperrung auf dem Server durch.
    
    Attributes:
        member (disnake.Member): Das Mitglied, das gebannt werden soll.
    """

    member: disnake.Member | None = None

    def __init__(self, member: disnake.Member):
        components = [
            disnake.ui.TextInput(
                label="Grund",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                value="Unangemessenes Verhalten"
            )
        ]
        self.member = member

        super().__init__(title=f"{member.global_name} banen", components=components)

    
    async def callback(self, inter: disnake.ModalInteraction):
        #Mitglied benachrichtigen
        await self.member.send(
            embed=disnake.Embed(
                title="Du wurdest gebannt",
                description=f"**Grund:**\n{inter.text_values.get("reason")}"
            )
        )

        #Das Mitglied bannen
        await self.member.ban(reason=inter.text_values.get("reason"))

        #Response
        await inter.response.send_message(
            f"Das Mitglied: **{self.member.global_name}** wurde erfolgreich gebannt.",
            ephemeral=True,
            delete_after=5
        )
