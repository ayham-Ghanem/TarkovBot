from ast import Delete, Num
from cgitb import text
from dis import disco
import imp
from re import I
from tkinter.ttk import Style
from turtle import update
import discord
import random
from .db1 import DB1
from discord.ext import commands, tasks
import os
from itertools import cycle
import asyncio
import aiomysql
from .queue1 import Queue1
import string
from discord.utils import get     
from discord_components import *
import Config






class Button_clicked(commands.Cog):

    def __init__(self,client):
        self.funtions_dict = self.get_dict()
        self.client = client
        self.myDB = DB1(self.client)
        self.queue = Queue1(self.client)
    
    
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

#-----------------------------------------------------------------------------------
    async def join_clicked(self,interaction):
        
        person = interaction.user
        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.respond(embed=embed) 
            return
        else:
            
             
            if not (self.queue.check_in_lst(person)):
                self.queue.lst_join(person)
                embed = discord.Embed(
                title=f"{person} Joined the queue",
                color = 0x0000ff) 
                await interaction.respond(embed=embed) 
            else:
                embed = discord.Embed(
                title=f"{person} already in  the queue",
                color = 0x0000ff)
                await interaction.respond(embed=embed)

        await self.update_player_num(interaction)


    async def host_clicked(self,interaction):
        
        text_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_text_id())
        text_channel = await interaction.guild.create_text_channel(f'{interaction.user}', category=text_category)

        components = [Button(style=ButtonStyle.green,label='Join',custom_id="Join"),
                    Button(style=ButtonStyle.red,label="Leave",custom_id="Leave"),
                    Button(style=ButtonStyle.grey,label="Close Channel",custom_id="Close_Channel")]
        embed = discord.Embed(
        title=f"{interaction.user} lobby",
        description="",
        color = 0xffffff)
        await text_channel.send(embed=embed,components=components)

        voice_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_voice_id())
        await interaction.guild.create_voice_channel(f'{interaction.user}', category=voice_category)
       
       
        embed = discord.Embed(
            title="Now you have text and voice channels",
            color = 0xffff00)  
        await interaction.respond(embed=embed) 

        

    async def Leave_clicked(self,interaction):
        
        person = interaction.user
        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.respond(embed=embed) 
            return
        else:
            if(self.queue.check_in_lst(person)):
                self.queue.lst_leave(person)
                await self.update_player_num(interaction)
                embed = discord.Embed(
                title=f"{person} Left the queue",
                color = 0x0000ff)  
                await interaction.respond(embed=embed) 
            else:
                embed = discord.Embed(
                title=f"{person} not in the queue",
                color = 0xffff00)  
                await interaction.respond(embed=embed)
                return
            
        
    async def Close_Channel_clicked(self,interaction):
        channel_name = interaction.channel.name[0:-4] + '#' + interaction.channel.name[-4:]
        if channel_name != str(interaction.user).lower():
            embed = discord.Embed(
            title=f"Only the host can close the channel",
            color = 0xff00)  
            await interaction.channel.send(embed=embed)
            return
        embed = discord.Embed(
            title=f"GGs everyone",
            color = 0xffff00)  
        embed1 = discord.Embed(
            title=f"hope you enjoyed :)",
            color = 0xffffff)  
        await interaction.respond(embed=embed1)
        await interaction.channel.send(embed=embed)
        voice_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_voice_id())
    
        for i in voice_category.voice_channels:
            if i.name == str(interaction.user):
                voice_channel = i
                break
        
        
        await asyncio.sleep(6)
        await voice_channel.delete()
        await interaction.channel.delete()

            

    async def update_player_num(self,interaction):

        players_num = len(self.queue.get_lst())

        embed1 = discord.Embed(
        title="Queue channel",
        description=f"players in queue: {players_num}/100",
        color = 0x00ffff
    )
        components1 = [Button(style=ButtonStyle.green,label='Join',custom_id="Join"),
                    Button(style=ButtonStyle.red,label="Leave",custom_id="Leave")]

        await interaction.message.edit(embed = embed1, components=components1)
    


    def get_dict(self):
        return {"Register":self.Register_clicked,'Change_username':self.Change_username_clicked,'Join':self.join_clicked,'Leave': self.Leave_clicked,'Host':self.host_clicked,'Close_Channel':self.Close_Channel_clicked}

def setup(client):
    
    client.add_cog(Button_clicked(client))
   
    