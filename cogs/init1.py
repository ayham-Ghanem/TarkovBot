from ast import Num
from dis import disco
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
from discord_components import *
import Config


class Init(commands.Cog):

    def __init__(self,client):
       
        self.client = client

    @commands.command()
    async def init(self,ctx):
        channel_id = Config.get_register_channel()
        channel = ctx.guild.get_channel(int(channel_id)) 
        embed = discord.Embed(
        title="Welcome to custom games bot",
        description="make sure you register before you queue",
        color = 0x00ff00
    )
        components = [Button(style=ButtonStyle.green,label='Register',custom_id="Register"),
                    Button(style=ButtonStyle.blue,label="Change username",custom_id="Change_username")]
        
        
        await channel.send(embed = embed, components=components)

        channel_id = Config.get_queue_channel()
        channel1 = ctx.guild.get_channel(int(channel_id))
        embed1 = discord.Embed(
        title="Create lobby",
        description=f"Click Host to host a match",
        color = 0x00ffff
    )
        components1 = [Button(style=ButtonStyle.green,label='Host',custom_id="Host")]

        await channel1.send(embed = embed1, components=components1)








def setup(client):
    
    client.add_cog(Init(client))
    
  