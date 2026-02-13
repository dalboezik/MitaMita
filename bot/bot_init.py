#imports
import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[1452248096883867721])

