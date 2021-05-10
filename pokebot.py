import discord
from discord.ext import commands
import asyncio
import time
import globals
import logging
import db
import setuppk
from logging.handlers import RotatingFileHandler
from discord.utils import get


intents = discord.Intents(messages=True, guilds=True, members=True)


bot = commands.Bot(command_prefix='$', description='description here', intents=intents)
bot.remove_command('help')


handler = RotatingFileHandler('pokebot.log', maxBytes=10000000, backupCount=10)
logging.basicConfig(handlers=[handler], format='%(asctime)s %(message)s', level=logging.DEBUG)
bot.logger = logging.getLogger('bot')


extens = ['setuppk','battle','all','dice']
#extens = ['modbot', 'stats', 'greeter']

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    

@bot.event
async def on_ready():
    print("I'm in")
    print(bot.user)

if __name__ == "__main__":
    for extension in extens:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(globals.TOKEN)
