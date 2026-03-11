import disnake

from disnake.ext import commands

from bot_init import bot

class SelectChannelDropdown(disnake.ui.StringSelect):
    """
    A dropdown to select a channel where the embed should be sent:
    - Promts the user to select a channel.
    - Sends the embed to the selected channel.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
    """
    def __init__(self, message: disnake.Message):
        self.message = message
        options = [channel.name for channel in bot.guilds[0].channels]

        super().__init__(
            placeholder="Select a channel", 
            min_values=1, 
            max_values=1, 
            options=options
        )


    async def callback(self, inter: disnake.MessageInteraction):
        """Sends the embed to the selected channel."""
        for channel in bot.guilds[0].channels:
            if channel.name == self.values[0]:
                await bot.get_channel(channel.id).send(embed=self.message.embeds[0])

        #Response ->
        await inter.response.send_message(
            f"The embed was successfully sent in the channel {self.values[0]}."
        )

        container = disnake.ui.Container(
            disnake.ui.TextDisplay("## Done?"),
            disnake.ui.TextDisplay("If you're done, you can delete the temporary channel."),
            disnake.ui.ActionRow(
                disnake.ui.Button(
                    label="Delete", 
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
        