#imports
from bot_init import bot

async def delete_chat_history(channel_id: int):
    """Löscht alle Nachrichten von dem Bot in dem Channel"""
    async for message in bot.get_channel(channel_id).history():
        if message.author == bot.user:
            await message.delete()