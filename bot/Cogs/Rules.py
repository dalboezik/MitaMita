#imports
import disnake

import config

from disnake.ext import commands

from bot_init import bot
from utils.delete_chat_history import delete_chat_history


class Rules(commands.Cog):
    """Schickt einen Embed mit den Regeln"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def sendRules():
        #Embed ->
        '''
        embed = disnake.Embed(title="Regeln")

        counter = 1
        for rule in config.RULES_JSON:
            embed.add_field(name=f"__{counter}. {rule["title"]}__", value=rule["description"], inline=False)
            counter += 1

        embed.add_field(name="", value="> _Unwissenheit schützt vor der Strafe NICHT!_")

        await delete_chat_history(config.RULES_CHANNEL_ID)

        await bot.get_channel(config.RULES_CHANNEL_ID).send(embed=embed, components=[
            disnake.ui.Button(
                label="Einverstanden",
                custom_id="accept_rules",
                style=disnake.ButtonStyle.green
            )
        ])
        '''
        
        #Container ->
        rules: list[disnake.ui.TextDisplay] = [
            disnake.ui.TextDisplay(f"### {rule.get('title', '')}\n{rule.get('description', '')}") 
            for rule in config.RULES_JSON
        ]

        container = disnake.ui.Container(disnake.ui.TextDisplay("## Regeln"), *rules)

        await delete_chat_history(config.RULES_CHANNEL_ID)
        await bot.get_channel(config.RULES_CHANNEL_ID).send(
            components=[
                container,
                disnake.ui.Button(
                    label="Einverstanden",
                    custom_id="accept_rules",
                    style=disnake.ButtonStyle.green
                )
            ]
        )

    @commands.Cog.listener("on_button_click")
    async def accept_rules(self, inter: disnake.MessageInteraction):
        """Gibt dem user die member role, wenn er die regeln akzeptiert hat"""
        await inter.response.defer(ephemeral=True)

        if inter.component.custom_id == "accept_rules":
            await inter.author.add_roles(inter.guild.get_role(config.MEMBER_ROLE_ID))


def setup(bot: commands.Bot):
    bot.add_cog(Rules(bot))