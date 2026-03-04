#imports
import disnake


class RemoveFieldDropdown(disnake.ui.StringSelect):

    def __init__(self, message: disnake.Message):
        self.message = message
        options = [
            disnake.SelectOption(
                label=field.name, 
                description=field.value
            ) 
            for field in self.message.embeds[0].fields
        ]

        super().__init__(placeholder="", max_values=1, min_values=1, options=options)


    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.defer(ephemeral=True)

        for index, value in enumerate(self.message.embeds[0].fields):
            if str(value.name) == str(self.values[0]):
                self.message.embeds[0].remove_field(index)
                break
        
        await self.message.edit(embed=self.message.embeds[0])
        await inter.followup.send("The field was deleted", ephemeral=True, delete_after=5)       


class DropDownView(disnake.ui.View):
    def __init__(self, message: disnake.Message):

        super().__init__()

        self.add_item(RemoveFieldDropdown(message=message))
