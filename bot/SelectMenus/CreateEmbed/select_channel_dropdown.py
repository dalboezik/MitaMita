import disnake

from disnake.ext import commands

from bot_init import bot

class SelectChannelDropdown(disnake.ui.StringSelect):
    def __init__(self, message: disnake.Message):
        self.message = message
        options = [channel.name for channel in bot.guilds[0].channels]

        super().__init__(
            placeholder="wähle ein channel", 
            min_values=1, 
            max_values=1, 
            options=options
        )


    async def callback(self, inter: disnake.MessageInteraction):
        for channel in bot.guilds[0].channels:
            if channel.name == self.values[0]:
                await bot.get_channel(channel.id).send(embed=self.message.embeds[0])

        await inter.response.send_message("Dein Embed wurde erfolgreich erstellt.")

        container = disnake.ui.Container(
            disnake.ui.TextDisplay("## Fertig?"),
            disnake.ui.TextDisplay("Wenn du fertig bist, kannst du diesen Channel löschen."),
            disnake.ui.ActionRow(
                disnake.ui.Button(
                    label="Löschen", 
                    custom_id="delete_channel",
                    style=disnake.ButtonStyle.danger
                )
            )
        )

        await inter.followup.send(components=[container])


class DropDownView(disnake.ui.View):
    def __init__(self, message: disnake.Message):
        super().__init__()

        self.add_item(SelectChannelDropdown(message=message))        
        