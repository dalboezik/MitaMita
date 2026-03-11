# imports
import disnake
from bot_init import bot

class TimeoutModal(disnake.ui.Modal):
    """
    A modal window for timing out a member.

    This modal allows moderators to specify a duration in minutes and a reason. 
    The duration input is validated to ensure it can be converted to a 
    numeric format.

    Attributes:
        member (disnake.Member): Das Mitglied, das stummgeschaltet werden soll.
    """

    member: disnake.Member | None = None

    def __init__(self, member: disnake.Member):
        components = [
            disnake.ui.TextInput(
                label="Duration (Min)",
                custom_id="duration",
                value="5"
            ),
            disnake.ui.TextInput(
                label="Reason",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                value="Inappropriate behavior"
            )
        ]
        self.member = member

        super().__init__(title=f"Timing out {self.member.global_name}", components=components)

    
    async def callback(self, inter: disnake.ModalInteraction):
        try:
            #If the entered duration is more than 28 days
            #(Discord supports max. timeout of 28 days)
            if float(inter.text_values.get("duration").replace(",", ".")) > 40320.0:
                await inter.response.send_message(
                    "The entered duration is too high",
                    ephemeral=True,
                    delete_after=5
                )
                return
            
            #Setting timeout
            await self.member.timeout(
                duration=float(inter.text_values.get("duration").replace(",", "."))*60, 
                reason=inter.text_values.get("reason")
            )

            #Response
            await inter.response.send_message(
                f"{self.member.global_name} has been timed out " + 
                f"for {inter.text_values.get("duration")} minutes.",
                ephemeral=True,
                delete_after=5
            )
        except ValueError as err:
            #Error message for invalid characters in the duration input.
            await inter.response.send_message(
                f"Invalid characters '{inter.text_values.get("duration")}' are not supported.",
                ephemeral=True,
                delete_after=8
            )
