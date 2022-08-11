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
from discord.ui import *
import Config




class DB1(commands.Cog):

    def __init__(self,client):
        self.client = client

    async def in_dms(self, interaction):
        
        person = interaction.user
        embed = discord.Embed(
        title="Please enter you're EFT username",
        color = 0x00ff00
    )   
        def check(msg):                           
            return msg.content and msg.author.id != 1005511022964125798 and msg.author == person
        await person.send(embed=embed)
        msg = await self.client.wait_for('message', check=check)
        player_username = str(msg.content.upper().replace(' ', ''))
        if not (await self.check_by_name(player_username)):
            embed = discord.Embed(
            title="This name is already taken... please try again",
            color = 0xffff00)
            return None

        return player_username



    async def register(self,interaction):
        person = interaction.user
        myDB = await aiomysql.connect(host='localhost',user='root',password='ayham123123',db='treydb')
        player_username = await self.in_dms(interaction)
        if player_username == None:
            return
        #registration process
        async with myDB.cursor() as cur:
            await cur.execute(f"INSERT INTO `players`(`player`, `username`) VALUES ('{person.id}','{player_username}')")
            await myDB.commit()
            embed = discord.Embed(
            title=f"Successfully Registered as {player_username}",
            color = 0xffffff)
            await person.send(embed=embed)
       


    #returns true if the player is not in the database
    async def check_by_id(self,person):
        
        myDB= await aiomysql.connect(host='localhost',user='root',password='ayham123123',db='treydb')
        async with myDB.cursor() as cur:
            await cur.execute(f"SELECT `player` FROM `players` WHERE player = '{person.id}'")
            res = await cur.fetchall()
            return res == ()
            
    #returns true if the player's username is not in the database
    async def check_by_name(self,username):
        
        myDB= await aiomysql.connect(host='localhost',user='root',password='ayham123123',db='treydb')
        async with myDB.cursor() as cur:
            await cur.execute(f"SELECT `username` FROM `players` WHERE username = '{username}'")
            res = await cur.fetchall()
            return res == ()



           



    async def change_username(self,interaction):
        person = interaction.user
        myDB= await aiomysql.connect(host='localhost',user='root',password='ayham123123',db='treydb')
        player_username = await self.in_dms(interaction)
        if player_username == None:
            return
        
        async with myDB.cursor() as cur:
            await cur.execute(f"UPDATE `players` SET `username`= '{player_username}' WHERE player = '{person.id}'")
            await myDB.commit()
            embed = discord.Embed(
            title=f"Successfully Registered as {player_username}",
            color = 0xffffff)
            await person.send(embed=embed)
        







async def setup(client):
    
    await client.add_cog(DB1(client))