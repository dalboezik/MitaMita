#imports
from bot_init import bot

async def delete_chat_history(channel_id: int):
    """Deletes all messages sent by the bot in the channel."""
    async for message in bot.get_channel(channel_id).history():
        if message.author == bot.user:
            await message.delete()