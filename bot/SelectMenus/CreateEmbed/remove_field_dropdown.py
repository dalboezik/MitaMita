#imports
import disnake


class RemoveFieldDropdown(disnake.ui.StringSelect):
    """
    A dropdown to remove fields:
    - Prompts the user to select the field that should be deleted.
    - Deletes the selected field from the embed.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
    """

    def __init__(self, message: disnake.Message):
        self.message = message
        options = [
            disnake.SelectOption(
                label=field.name, 
                description=field.value
            ) 
            for field in self.message.embeds[0].fields
        ]

        super().__init__(
            placeholder="Select the field that should be removed.", 
            max_values=1, 
            min_values=1, 
            options=options
        )


    async def callback(self, inter: disnake.MessageInteraction):
        """Removes the selected field."""
        await inter.response.defer(ephemeral=True)

        for index, value in enumerate(self.message.embeds[0].fields):
            if str(value.name) == str(self.values[0]):
                self.message.embeds[0].remove_field(index)
                break
        
        await self.message.edit(embed=self.message.embeds[0])
        await inter.followup.send(
            "The field was successfully removed.", 
            ephemeral=True, 
            delete_after=5
        )       


class DropDownView(disnake.ui.View):
    def __init__(self, message: disnake.Message):

        super().__init__()

        self.add_item(RemoveFieldDropdown(message=message))
