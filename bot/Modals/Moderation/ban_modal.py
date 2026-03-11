# imports
import disnake
from bot_init import bot

class BanModal(disnake.ui.Modal):
    """
    An interactive modal window to confirm a ban.

    This modal prompts the moderator for a reason, notifies the affected 
    member via direct message, and subsequently executes the ban on the server.
    
    Attributes:
        member (disnake.Member): Das Mitglied, das gebannt werden soll.
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

        super().__init__(title=f"Ban {member.global_name}", components=components)

    
    async def callback(self, inter: disnake.ModalInteraction):
        #Notify the member
        await self.member.send(
            embed=disnake.Embed(
                title="You have been banned from the server.",
                description=f"**Reason:**\n{inter.text_values.get("reason")}"
            )
        )

        #Ban the member
        await self.member.ban(reason=inter.text_values.get("reason"))

        #Response
        await inter.response.send_message(
            f"Successfully banned **{self.member.global_name}**.",
            ephemeral=True,
            delete_after=5
        )
