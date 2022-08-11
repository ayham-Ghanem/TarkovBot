from ast import Num
from dis import disco
import queue
from tkinter.ttk import Style
import discord
import random
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio
import aiomysql
import string
from discord.utils import get    
import Config



intents = discord.Intents.all()
client = commands.Bot(command_prefix='.',case_insensitive=True ,intents =intents )
status = cycle(['.help for help', 'whatever','111111'])
#client.remove_command('help') 
print ('Starting.....')

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def aa(ctx):
    print('aa')
    await ctx.send('aa')

@client.event
async def on_ready():
   change_status.start()
   global queue_dict
   queue_dict = {}
   print('Bot is Ready.')

def get_queue_dict():
    return queue_dict

async def load(str):
    await client.load_extension(str)


@client.command()
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename.startswith('singleton1') or filename.startswith('queue1') :
            continue
        asyncio.run(load(f'cogs.{filename[:-3]}'))


key = Config.get_key()
client.run(key)
