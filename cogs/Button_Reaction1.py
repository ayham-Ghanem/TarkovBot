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
from discord.ui import *
import Config
from .singleton1 import *






class Button_clicked(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.myDB = DB1(self.client)
        self.queue_dict = Queue_dict()
        self.channels_dict = Channels_dict()
        
       
  
    async def Register_clicked(self,interaction):
        
        person = interaction.user

        if not (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="you already registered",
            color = 0xff0000)  
            #await interaction.response.send_message(embed=embed) 
            return
        else:
            embed = discord.Embed(
            title="Check you're DMs",
            color = 0x0000ff)  
            #await interaction.response.send_message(embed=embed) 

        try:
            await self.myDB.register(interaction)
        except:
            return
        

    async def Change_username_clicked(self,interaction):
        
        person = interaction.user
        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            #await interaction.response.send_message(embed=embed) 
            return
        else:
            embed = discord.Embed(
            title="Check you're DMs",
            color = 0x0000ff)  
            #await interaction.response.send_message(embed=embed) 



        await self.myDB.change_username(interaction)

#-----------------------------------------------------------------------------------
    async def join_clicked(self,interaction):
        await self.update_player_num(interaction)
        person = interaction.user

        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.response.send_message(embed=embed) 
            return
        else:
            
            host = self.channels_dict.find_by_value(interaction.channel_id)

            el_queue = self.queue_dict.get_queue(host)
            if el_queue == None:
                print('el_queue == None')
                return
             
            if not (el_queue.check_in_lst(person)):
                el_queue.lst_join(person)
                embed = discord.Embed(
                title=f"{person} Joined the queue",
                color = 0x0000ff) 
                await interaction.response.send_message(embed=embed) 
            else:
                embed = discord.Embed(
                title=f"{person} already in  the queue",
                color = 0x0000ff)
                await interaction.response.send_message(embed=embed)
        
        await self.update_player_num(interaction)


    async def host_clicked(self,interaction):
        


        person = interaction.user
        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            #await interaction.response.send_message(embed=embed) 
            return
        
    
        text_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_text_id())
        text_channel = await interaction.guild.create_text_channel(f'{interaction.user}', category=text_category)

        view = Host_Menu(self.client)
        embed = discord.Embed(
        title=f"{interaction.user} lobby",
        description="",
        color = 0xffffff)
        await text_channel.send(embed=embed, view = view)

        my_queue = Queue1(self.client,interaction,text_channel)

        voice_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_voice_id())
        await interaction.guild.create_voice_channel(f'{interaction.user}', category=voice_category)
       
       
        embed = discord.Embed(
            title="Now you have text and voice channels",
            color = 0xffff00)  
        #await interaction.response.send_message(embed=embed) 

        

    async def Leave_clicked(self,interaction):
        
        await self.update_player_num(interaction)
        person = interaction.user
        if (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            msg = await interaction.response.send_message(embed=embed) 
            
            return
        else:
            host = self.channels_dict.find_by_value(interaction.channel_id)
            el_queue = self.queue_dict.get_queue(host)
            if el_queue == None:
                print('el_queue == None')
                return
            if(el_queue.check_in_lst(person)):
                
                embed = discord.Embed(
                title=f"{person} Left the queue",
                color = 0x0000ff)  
                msg = await interaction.response.send_message(embed=embed) 
                el_queue.lst_leave(person)
                await self.update_player_num(interaction)
                # await asyncio.sleep(2)
                # await msg.delete()
            else:
                embed = discord.Embed(
                title=f"{person} not in the queue",
                color = 0xffff00)  
                await interaction.response.send_message(embed=embed)
                return
            
        
    async def Close_Channel_clicked(self,interaction):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
            title=f"Only the host can close the channel",
            color = 0xff00)  
            await interaction.channel.send(embed=embed)
            return
        await interaction.message.delete() 
        embed = discord.Embed(
            title=f"GGs everyone",
            color = 0xffff00)  
        embed1 = discord.Embed(
            title=f"hope you enjoyed :)",
            color = 0xffffff)  
        await interaction.response.send_message(embed=embed1)
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

        host = self.channels_dict.find_by_value(interaction.channel_id)
        el_queue = self.queue_dict.get_queue(host)
        if el_queue == None:
            print('el_queue == None')
            return
        
            

        players_num = len(el_queue.get_lst())
        view = Host_Menu(self.client)
        embed1 = discord.Embed(
        title="Queue channel",
        description=f"players in queue: {players_num}/10",
        color = 0x00ffff
    )

        await interaction.message.edit(embed = embed1, view=view)
    


class Host_Menu(discord.ui.View):

    def __init__(self,client):
        
        super().__init__()
        self.client = client
        self.button = Button_clicked(self.client)
        self.value = None

    @discord.ui.button(label='Join' ,style=discord.ButtonStyle.green)
    async def Join(self,interaction:discord.Interaction, button: discord.ui.Button ):
        await self.button.join_clicked(interaction)
        
   
    @discord.ui.button(label='Leave' ,style=discord.ButtonStyle.danger)
    async def Leave(self, interaction:discord.Interaction, button: discord.ui.Button):
        
        await self.button.Leave_clicked(interaction)

    @discord.ui.button(label='Game Modes' ,style=discord.ButtonStyle.blurple)
    async def game_mode(self, interaction:discord.Interaction, button: discord.ui.Button):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
            title=f"Only the host can add limits",
            color = 0xff00)  
            await interaction.channel.send(embed=embed)
            return

        await interaction.response.send_modal(Host_modal())

    @discord.ui.button(label='Close Channel' ,style=discord.ButtonStyle.grey)
    async def Close_channel(self, interaction:discord.Interaction, button: discord.ui.Button):
        
        await self.button.Close_Channel_clicked(interaction)


class Host_modal(discord.ui.Modal,title= 'Game mode / limits?'):

    
    answer = discord.ui.TextInput(label='any game modes?',style=discord.TextStyle.paragraph,placeholder='no 7.62 BP\nNo Pistols',required= False)


    async def on_submit(self,interaction: discord.Interaction):
        
        if self.answer.value == '':
            embed = discord.Embed(title= 'No Limits',description='' ,color=discord.Color.random())
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(title= 'Game modes / limits',description=self.answer ,color=discord.Color.random())
        await interaction.response.send_message(embed=embed)

          

async def setup(client):
    
    await client.add_cog(Button_clicked(client))
   
    