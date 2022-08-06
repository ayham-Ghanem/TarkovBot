import discord
import random
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio
import aiomysql
import string
from discord.utils import get   
import Key


client = commands.Bot(command_prefix='.')
status = cycle(['.help for help', 'whatever','111111'])
#client.remove_command('help') 
print ('Starting.....')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
   change_status.start()
   print('Bot is Ready.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



key = Key.get_key()
client.run(key)
