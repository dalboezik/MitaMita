#imports
import disnake

import config

from bot_init import bot
from Cogs.CreateEmbed import CreateEmbed
from Cogs.Rules import Rules
from Cogs.Ticket import Ticket
from utils.load_cogs import load_cogs

def main():

    @bot.event
    async def on_ready():
        load_cogs()
        if config.RULES_ENABLE:
            await Rules.sendRules()
        if config.TICKET_ENABLE:
            await Ticket.sendTicketEmbed()
        if config.CREATEEMBED_ENABLE:
            await CreateEmbed.send_init_container()

        print(f"{bot.user} is online!")


    bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
    main()
