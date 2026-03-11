# imports
import disnake

import config
import temp

from disnake.ext import commands

from bot_init import bot
from Modals.Voicechannel.rename_modal import RenameModal
from Modals.Voicechannel.set_limit_modal import SetLimitModal


class VoiceChannel(commands.Cog):
    """
    A Cog for the dynamic management of voice channels (Temp Channels).

    This class allows users to create temporary voice channels by joining a 
    designated 'Join-to-Create' channel. It provides features for the automatic 
    deletion of empty channels, transferring channel ownership, and editing 
    channel properties via modals or slash commands.

    Attribute:
        bot (commands.Bot): Die Instanz des Discord-Bots.
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(
        self, 
        member: disnake.Member, 
        before: disnake.VoiceState, 
        after: disnake.VoiceState
    ):
        """
        Monitors voice state updates to:
        1. Create new temporary channels when the 'Join-to-Create' channel is joined.
        2. Delete empty temporary channels.
        3. Transfer channel ownership if the creator leaves the channel.
        """

        if before.channel != None and before.channel != after.channel:
            if before.channel.id != config.VOICE_CHANNEL_ID:
                if len(before.channel.members) == 0:
                    # Deletes an empty voicechannel
                    temp.voice_channels.pop(before.channel.id)
                    await before.channel.delete()
                elif member == member.guild.get_member(temp.voice_channels[before.channel.id].id):
                    # Transfer channel ownership if the creator leaves the channel
                    #print("Der Ersteller ist disconnected")
                    temp.voice_channels[before.channel.id] = before.channel.members[0]
            return   

        # Create a new temporary voicechannel
        if after.channel.id == config.VOICE_CHANNEL_ID:
            newVoiceChannel = await member.guild.create_voice_channel(
                name=f"{member.global_name}'s Voice Channel",
                category=disnake.utils.get(
                    member.guild.categories, 
                    id=config.VOICE_CHANNEL_CATEGORY_ID
                )
            )

            temp.voice_channels.update({newVoiceChannel.id: member})
            await member.move_to(newVoiceChannel)

            # Edit the voicechannel
            # Embed ->
            '''
            await newVoiceChannel.send(
                embed=disnake.Embed(title="Manage the voice channel"), 
                components=[
                    disnake.ui.Button(
                        label="Rename",
                        custom_id="rename_btn",
                    ),
                    disnake.ui.Button(
                        label="Set Limit",
                        custom_id="set_limit_btn"
                    )
                ]
            )
            '''
            
            # Container ->
            container = disnake.ui.Container(
                disnake.ui.TextDisplay(
                    "### Manage the voice channel"
                ),
                disnake.ui.ActionRow(
                    disnake.ui.Button(
                        label="Rename",
                        custom_id="rename_btn",
                        style=disnake.ButtonStyle.green
                    ),
                    disnake.ui.Button(
                        label="Set Limit",
                        custom_id="set_limit_btn",
                        style=disnake.ButtonStyle.blurple
                    )
                )
            )

            await newVoiceChannel.send(components=[container])


    # Modals to manage the voice channel
    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        """
        Processes interactions with the voice channel control buttons to manage 
        the channel. Opens the corresponding modals.
        """

        if inter.component.custom_id == "rename_btn":
            await inter.response.send_modal(RenameModal())
        elif inter.component.custom_id == "set_limit_btn":
            await inter.response.send_modal(SetLimitModal())
            

    # A slash command to manage the channel
    @commands.slash_command(
        name="voice_channel", 
        description="A slash command to manage the channel"
    )
    async def voice_channel(self, inter: disnake.CommandInteraction, option: str, argument: str):
        """
        Slash command for manual management of the temporary voice channel.

        Args:
            option (str): The property to be changed (rename, set_limit).
            argument (str): The new value for the selected option.
        """

        await inter.response.defer(ephemeral=True)

        # Check if the interaction author is in a voice channel.
        if inter.author.voice == None:
            await inter.followup.send("You must be in a voiche channel.")
            return

        # Checking if the user has permission to edit the channel.
        if not temp.voice_channels[inter.author.voice.channel.id] == inter.author:
            await inter.followup.send(
                content="You don't have the permissions to edit the voice channel.",
                ephemeral=True
            )
            return

        # Options
        if option == "rename":
            await inter.author.voice.channel.edit(name=argument)
            await inter.followup.send(
                content="The name of the channel has been successfully updated.", 
                ephemeral=True
            )
        elif option == "set_limit":
            await inter.author.voice.channel.edit(user_limit=int(argument))
            await inter.followup.send(
                "The user limit has been successfully updated.", 
                ephemeral=True
            )
        else:
            await inter.followup.send(f"'{option}': Unknown option.")


    #Autocompleting of the slash command
    @voice_channel.autocomplete("option")
    async def option_autocomplete(self, inter: disnake.CommandInteraction, user_input: str):
        options = ["rename", "set_limit"]

        #List comprehension
        #[expression for element in iterable if condition]
        #Returns the options that match the input.
        return [option for option in options if user_input.lower() in option.lower()][:25]


    #Errorhandling ->
    @voice_channel.error
    async def voice_channel_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("Only integers are allowed as input.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(VoiceChannel(bot))
