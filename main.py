import discord
from dotenv import load_dotenv

import os

from src import Bot


# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Not to create global commands so they can be updated instantly
GUILD_IDS = [int(x) for x in os.getenv('GUILD_IDS').split(',') if x]


# Create bot
bot = Bot(intents=discord.Intents.all(), debug_guilds=GUILD_IDS)

# Load cogs (extensions) to bot
for file in os.listdir('./cogs'):
    if file.endswith('.py') and not file.startswith('_'):
        bot.load_extension(f'cogs.{file[:-3]}')

# Run bot
bot.run(BOT_TOKEN)
