#imports
import disnake

import config

from disnake.ext import commands

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=config.GUILDS)
