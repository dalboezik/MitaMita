# imports
import disnake
from bot_init import bot

class KickModal(disnake.ui.Modal):
    """
    A modal window for the Discord member kick process.

    This modal allows administrators or moderators to provide a reason for the kick.
    Upon submission, the member is notified, and subsequently removed from the server..

    Attributes:
        member (disnake.Member): Das Mitglied, das gekickt werden soll.
    """

    member: disnake.Member | None = None

    def __init__(self, member: disnake.Member):
        components = [
            disnake.ui.TextInput(
                label="Reason",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                value="Inappropriate behavior"
            )
        ]
        self.member = member

        super().__init__(title=f"Kick {member.global_name}", components=components)


    async def callback(self, inter: disnake.ModalInteraction):
        #Notify the member
        await self.member.send(embed=disnake.Embed(
            title="You have been kicked from the server.",
            description=f"**Reason:**\n{inter.text_values.get("reason")}"
        ))

        #Kick the member
        await self.member.kick()

        #Response
        await inter.response.send_message(
            f"Successfully kicked **{self.member.global_name}**",
            ephemeral=True,
            delete_after=5
        )
