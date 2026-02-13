# imports
import disnake
from bot_init import bot

class KickModal(disnake.ui.Modal):
    """
    Ein modales Dialogfenster zum Kick-Prozess eines Discord-Mitglieds.

    Dieses Modal ermöglicht es Administratoren oder Moderatoren, einen Grund für 
    den Kick anzugeben. Nach dem Absenden wird das Mitglied benachrichtigt 
    und anschließend vom Server entfernt.

    Attributes:
        member (disnake.Member): Das Mitglied, das gekickt werden soll.
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

        super().__init__(title=f"Kick {member.global_name}", components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        #Mitglied benachrichtigen
        await self.member.send(embed=disnake.Embed(
            title="Du wurdest gekickt",
            description=f"**Grund:**\n{inter.text_values.get("reason")}"
        ))

        #Mitglied kicken
        await self.member.kick()

        #Response
        await inter.response.send_message(
            f"Der Member: **{self.member.global_name}** wurde erfolgreich gekickt.",
            ephemeral=True,
            delete_after=5
        )
