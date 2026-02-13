#imports
import config
import os
from bot_init import bot

def load_cogs():
    """Lädt alle Cogs, die auf True gestellt sind"""
    if os.path.exists(config.COGS_PATH):
        for file in os.listdir(config.COGS_PATH):
            if file.endswith(".py"):
                #getattr() ermöglicht den Zugriff auf Felder und Methoden mit dem Namen als String
                isAvailable: bool = getattr(config, f"{file.upper()[:-3]}_ENABLE", False)
                if isAvailable:
                    bot.load_extension(f"Cogs.{file[:-3]}")
        else:
            print("All cogs are loaded")
    else:
        print(f"\"{COGS_PATH}\" could not be found")
