from ast import Num
from atexit import register
from code import interact
from dis import disco
from http import client
import imp
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
from discord.ui import *
import Config
from .Button_Reaction1 import Button_clicked

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
      
        
        view = Register_Menu(self.client)
        await channel.send(embed = embed, view=view)

        channel_id = Config.get_create_lobby_channel()
        channel1 = ctx.guild.get_channel(int(channel_id))
        embed1 = discord.Embed(
        title="Create lobby",
        description=f"Click Host to create you're own text and voice channels\nif you can't host make sure you register",
        color = 0x00ffff
    )
        
        view1 = Create_lobby_Menu(self.client)
        await channel1.send(embed = embed1, view=view1)





class Create_lobby_Menu(discord.ui.View):

    def __init__(self,client):
        
        super().__init__()
        self.client = client
        self.button = Button_clicked(self.client)
        self.value = None


    @discord.ui.button(label='Host' ,style=discord.ButtonStyle.green,custom_id="Host")
    async def Host(self,interaction:discord.Interaction, button: discord.ui.Button ):
       
        await self.button.host_clicked(interaction)
        
    




class Register_Menu(discord.ui.View):

    def __init__(self,client):
        
        super().__init__()
        self.client = client
        self.button = Button_clicked(self.client)
        self.value = None

    @discord.ui.button(label='Register' ,style=discord.ButtonStyle.green)
    async def register(self,interaction:discord.Interaction, button: discord.ui.Button ):
        
        await self.button.Register_clicked(interaction)
        
       


    @discord.ui.button(label='Change username' ,style=discord.ButtonStyle.blurple)
    async def Change_username(self, interaction:discord.Interaction, button: discord.ui.Button):
        await self.button.Change_username_clicked(interaction)
      


async def setup(client):
    
    await client.add_cog(Init(client))

    
  