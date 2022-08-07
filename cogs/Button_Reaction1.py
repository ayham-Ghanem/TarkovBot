from ast import Num
from dis import disco
import imp
from tkinter.ttk import Style
import discord
import random
from .db1 import DB1
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio
import aiomysql
import string
from discord.utils import get     
from discord_components import *
import Config





class Button_clicked(commands.Cog):

    def __init__(self,client):
        self.funtions_dict = self.get_dict()
        self.client = client
        self.myDB = DB1(self.client)
    
    
    @commands.Cog.listener()
    async def on_button_click(self,interaction):
        if str(interaction.component.id) not in self.funtions_dict:
            return
        await self.funtions_dict.get(str(interaction.component.id))(interaction)



    async def Register_clicked(self,interaction):
        
        person = interaction.user

        if not (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="you already registered",
            color = 0xff0000)  
            await interaction.respond(embed=embed) 
            return
        else:
            embed = discord.Embed(
            title="Check you're DMs",
            color = 0x0000ff)  
            await interaction.respond(embed=embed) 

        
        await self.myDB.register(interaction)
        

    async def Change_username_clicked(self,interaction):
        
        person = interaction.user
        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.respond(embed=embed) 
            return
        else:
            embed = discord.Embed(
            title="Check you're DMs",
            color = 0x0000ff)  
            await interaction.respond(embed=embed) 



        await self.myDB.change_username(interaction)


    async def join_clicked(self,interaction):
        print(interaction.component.id)

    async def Leave_clicked(self,interaction):
        print(interaction.component.id)
    


    def get_dict(self):
        return {"Register":self.Register_clicked,'Change_username':self.Change_username_clicked,'Join':self.join_clicked,'Leave': self.Leave_clicked}

def setup(client):
    
    client.add_cog(Button_clicked(client))
    