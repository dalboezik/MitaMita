#imports
import disnake

class RemoveFieldDropdown(disnake.ui.StringSelect):

    embed: disnake.Embed | None = None

    def __init__(self, embed: disnake.Embed):
        self.embed = embed
        options = [
            disnake.SelectOption(
                label=field.name, 
                description=field.value
            ) 
            for field in embed.fields
        ]
        super().__init__(placeholder="", max_values=1, min_values=1, options=options)

    #!!!Callback funktioniert nicht!!!
    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.defer(ephemeral=True)
        print(self.values)
        print(self.values[0])
        embed = self.embed.remove_field()
        await inter.response.send_message("BLYAT")
