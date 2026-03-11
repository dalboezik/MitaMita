#imports
import config
import os
from bot_init import bot

def load_cogs():
    """Loads all cogs where the value is set to True."""
    if os.path.exists(config.COGS_PATH):
        for file in os.listdir(config.COGS_PATH):
            if file.endswith(".py"):
                #getattr() allows access to object attributes and methods using their name as a string.
                isAvailable: bool = getattr(config, f"{file.upper()[:-3]}_ENABLE", False)
                if isAvailable:
                    bot.load_extension(f"Cogs.{file[:-3]}")
        else:
            print("All cogs are loaded")
    else:
        print(f"\"{COGS_PATH}\" could not be found")
