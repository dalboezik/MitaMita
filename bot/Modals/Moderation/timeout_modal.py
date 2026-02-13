# imports
import disnake
from bot_init import bot

class TimeoutModal(disnake.ui.Modal):
    """
    Ein Modal-Fenster zur zeitlich begrenzten Stummschaltung (Timeout) eines Mitglieds.
    
    Dieses Modal ermöglicht es Moderatoren, eine Dauer in Minuten sowie einen 
    Grund anzugeben. Die Eingabe der Dauer wird validiert, um sicherzustellen, 
    dass sie in ein numerisches Format umgewandelt werden kann.

    Attributes:
        member (disnake.Member): Das Mitglied, das stummgeschaltet werden soll.
    """

    member: disnake.Member | None = None

    def __init__(self, member: disnake.Member):
        components = [
            disnake.ui.TextInput(
                label="Dauer (in Minuten)",
                custom_id="duration",
                value="5"
            ),
            disnake.ui.TextInput(
                label="Grund",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                value="Unangemessenes Verhalten"
            )
        ]
        self.member = member

        super().__init__(title=f"{self.member.global_name} timeouten", components=components)

    
    async def callback(self, inter: disnake.ModalInteraction):
        try:
            #Wenn die eingegebene Dauer höher als 28 Tage ist
            #(Discord unterstützt einen max. Timeout von 28 Tagen)
            if float(inter.text_values.get("duration").replace(",", ".")) > 40320.0:
                await inter.response.send_message(
                    "Die eingegebene Dauer ist zu hoch.",
                    ephemeral=True,
                    delete_after=5
                )
                return
            
            #Timeout setzen
            await self.member.timeout(
                duration=float(inter.text_values.get("duration").replace(",", "."))*60, 
                reason=inter.text_values.get("reason")
            )

            #Response
            await inter.response.send_message(
                f"{self.member.global_name} darf {inter.text_values.get("duration")} "+
                f"Minuten lang über sein Verhalten nachdenken.",
                ephemeral=True,
                delete_after=5
            )
        except ValueError as err:
            #Fehlermeldung, wenn in der Dauereingabe Sonderzeichen auftauchen
            await inter.response.send_message(
                "Bei der Dauereingabe werden Ganz- oder Kommazahlen erwartet",
                ephemeral=True,
                delete_after=8
            )
