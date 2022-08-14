import time
import discord
from .db1 import DB1
from discord.ext import commands
import asyncio
from .queue1 import Queue1     
from discord.ui import *
import Config
from .singleton1 import *






class Button_clicked(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.pics = Config.get_maps_pics()
        self.myDB = DB1(self.client)
        self.queue_dict = Queue_dict()
        self.channels_dict = Channels_dict()
        
       
  
    async def Register_clicked(self,interaction):
        
        person = interaction.user

        if not (await self.myDB.check_by_id(person)):
            
            embed = discord.Embed(
            title="you already registered",
            color = 0xff0000)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            return
        else:
            embed = discord.Embed(
            title="Check you're DMs",
            color = 0x0000ff)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 

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
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            return
        else:
            embed = discord.Embed(
            title="Check you're DMs",
            color = 0x0000ff)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 



        await self.myDB.change_username(interaction)

#-----------------------------------------------------------------------------------
    async def join_clicked(self,interaction):
        

        if (await self.myDB.check_by_id(interaction.user)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            return
        else:
            
            host = self.channels_dict.find_by_value(interaction.channel_id)

            el_queue = self.queue_dict.get_queue(host)
            if el_queue == None:
                return
             
            if not (el_queue.check_in_lst(interaction.user)):
                el_queue.lst_join(interaction.user)
                embed = discord.Embed(
                title=f"{interaction.user} Joined the queue",
                color = 0x0000ff) 
                msg = await interaction.channel.send(embed=embed)
                await self.update_main_msg(interaction)
                await asyncio.sleep(2)
                await msg.delete()
            else:
                embed = discord.Embed(
                title=f"{interaction.user} already in  the queue",
                color = 0x0000ff)
                await interaction.response.send_message(embed=embed,ephemeral=True)

        


    async def host_clicked(self,interaction):
        
        

       
        
        
        if (await self.myDB.check_by_id(interaction.user)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            return
        host_set = Hosts_set()
        if(host_set.check_if_hosting(interaction.user.id)):
            embed = discord.Embed(
            title="You can't host more than one match",
            color = 0xffff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            return
        
    
        text_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_text_id())
        text_channel = await interaction.guild.create_text_channel(f'{interaction.user}', category=text_category)

        view = Host_Menu(self.client)
        embed = discord.Embed(
        title=f"1 man squad",
        description="Queue size = 10\n",
        color = 0xffffff)
        embed.set_author(name=interaction.user)
        embed.set_image(url='https://cdn.discordapp.com/attachments/487658114464612352/1008024714897260554/download.png')
        embed.set_thumbnail(url=interaction.user.display_avatar)
        msg = await text_channel.send(embed=embed, view = view)
        await msg.pin()

        

        host_set.add(interaction.user.id)
        my_queue = Queue1(self.client,interaction,text_channel,10,msg.id)

        voice_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_voice_id())
        await interaction.guild.create_voice_channel(f'{interaction.user}', category=voice_category)

        embed = discord.Embed(
            title="Now you have text and voice channels",
            color = 0xffff00)  
        await interaction.response.send_message(embed=embed,ephemeral=True)
       
       


    async def Leave_clicked(self,interaction):
        
        if (await self.myDB.check_by_id(interaction.user)):
            
            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            
            return
        else:
            host = self.channels_dict.find_by_value(interaction.channel_id)
            el_queue = self.queue_dict.get_queue(host)

            if(el_queue.check_in_lst(interaction.user)):
                
                el_queue.lst_leave(interaction.user)
                embed = discord.Embed(
                title=f"{interaction.user} Left the queue",
                color = 0x0000ff)  
                msg = await interaction.channel.send(embed=embed) 
                await self.update_main_msg(interaction)
                await asyncio.sleep(2)
                await msg.delete()
        
            else:
                embed = discord.Embed(
                title=f"{interaction.user} did not join the queue",
                color = 0xffff00)  
                await interaction.response.send_message(embed=embed,ephemeral=True)
                return
            


        
    async def Close_Channel_clicked(self,interaction):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
            title=f"Only the host can close the channel",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return
        
        host_set = Hosts_set()
        host_set.remove(interaction.user.id)

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
        
        
        await asyncio.sleep(5)
        await voice_channel.delete()
        await interaction.channel.delete()
    
    #map selected
    async def selected(self,interaction,select):

        map = select.values[0]
        await interaction.message.delete()
        host = self.channels_dict.find_by_value(interaction.channel_id)
        el_queue = self.queue_dict.get_queue(host)
        el_queue.change_map(map)
        await self.update_main_msg(interaction)


    async def squads_selected(self,interaction,select):
       
        number = int(select.values[0][0])
        await interaction.message.delete()
        host = self.channels_dict.find_by_value(interaction.channel_id)
        el_queue = self.queue_dict.get_queue(host)
        el_queue.change_players_in_team(number)
        await self.update_main_msg(interaction)
    

        
    async def queue_size_selected(self,interaction,answer):
    
        host = self.channels_dict.find_by_value(interaction.channel_id)
        el_queue = self.queue_dict.get_queue(host)
        el_queue.change_queue_size(int(answer.value))
        await self.update_main_msg(interaction)
        
        
    async def change_game_mode(self,interaction,answer):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        el_queue = self.queue_dict.get_queue(host)
        
        if answer.value == '':
            return
        el_queue.game_mode = answer
        await self.update_main_msg(interaction)
        
        

        
        


            
    
    async def update_main_msg(self,interaction):

        host_id = self.channels_dict.find_by_value(interaction.channel_id)
        host = await self.client.fetch_user(host_id)
        el_queue = self.queue_dict.get_queue(host_id)
        if el_queue == None:
            # print('el_queue == None')
            return

        # start = time.time()

        embed = discord.Embed(
            title = f'{el_queue.players_in_team} man squad',
            description= f'Queue size = {int(el_queue.queue_size)}\n',
            color = discord.Colour.random())
        embed.set_author(name=host)
        embed.set_image(url=self.pics.get(el_queue.map))
        embed.set_thumbnail(url=host.display_avatar)
        for i in el_queue.queue_lst:
            user = await self.client.fetch_user(i)
            embed.add_field(name=' ㅤ\n',value= user.mention)
        
        embed.add_field(name= 'Game mode / limits: ', value=el_queue.game_mode,inline=False)


        view = Host_Menu(self.client)
        msg = await interaction.channel.fetch_message(el_queue.msg_id)
        await msg.edit(embed = embed, view=view)
        # end = time.time()
        # print(end - start)
    

#----------------------------------------------------------------------------------------------------x
class Host_Menu(discord.ui.View):

    def __init__(self,client):
        
        super().__init__(timeout=None)
        self.client = client
        self.button = Button_clicked(self.client)
        self.value = None
        self.channels_dict = Channels_dict()

    @discord.ui.button(label='Join' ,style=discord.ButtonStyle.green)
    async def Join(self,interaction:discord.Interaction, button: discord.ui.Button ):
        await self.button.join_clicked(interaction)
        
   
    @discord.ui.button(label='Leave' ,style=discord.ButtonStyle.danger)
    async def Leave(self, interaction:discord.Interaction, button: discord.ui.Button):
        
        await self.button.Leave_clicked(interaction)


    @discord.ui.button(label='Select map' ,style=discord.ButtonStyle.blurple)
    async def Select_map(self, interaction:discord.Interaction, button: discord.ui.Button):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if (interaction.user.id != host):
            embed = discord.Embed(
            title=f"Only the host can select map",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        maps_view = Maps_select_view(self.client)
        await interaction.channel.send(view = maps_view)


    @discord.ui.button(label='Squads' ,style=discord.ButtonStyle.blurple)
    async def Select_squad(self, interaction:discord.Interaction, button: discord.ui.Button):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if (interaction.user.id != host):
            embed = discord.Embed(
            title=f"Only the host can change squads",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return
        squad_view = Squad_select_view(self.client)
        await interaction.channel.send(view = squad_view)


    @discord.ui.button(label='Queue size' ,style=discord.ButtonStyle.blurple)
    async def Select_Queue(self, interaction:discord.Interaction, button: discord.ui.Button):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if (interaction.user.id != host):
            embed = discord.Embed(
            title=f"Only the host can Queue size",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        await interaction.response.send_modal(Queue_size_Modal())



    @discord.ui.button(label='Game Modes' ,style=discord.ButtonStyle.blurple)
    async def game_mode(self, interaction:discord.Interaction, button: discord.ui.Button):
        channels_dict = Channels_dict()
        host = channels_dict.find_by_value(interaction.channel.id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
            title=f"Only the host can add limits",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        await interaction.response.send_modal(Game_mode_Modal())

    @discord.ui.button(label='Close Channel' ,style=discord.ButtonStyle.grey)
    async def Close_channel(self, interaction:discord.Interaction, button: discord.ui.Button):
        
        await self.button.Close_Channel_clicked(interaction)

#TODO: add to the main message (addfield)
class Game_mode_Modal(discord.ui.Modal,title= 'Game mode / limits?'):

   
    answer = discord.ui.TextInput(label='any game modes?',style=discord.TextStyle.paragraph,placeholder='no 7.62 BP\nNo Pistols\nall customs dorms\n hide and seek?\n noobs only :)',required= False)


    async def on_submit(self,interaction: discord.Interaction):
        buttonR = Button_clicked(interaction.client)
        await interaction.response.send_message('done',ephemeral=True)
        await buttonR.change_game_mode(interaction,self.answer)


class Queue_size_Modal(discord.ui.Modal,title= 'Queue size'):

   
    answer = discord.ui.TextInput(label='2 digits num',style=discord.TextStyle.short,placeholder='10 by default',required= True,max_length=2)


    async def on_submit(self,interaction: discord.Interaction):
        buttonR = Button_clicked(interaction.client)
        if not self.answer.value.isdigit():
            await interaction.response.send_message('please enter numbers only', ephemeral= True)
            return
        await interaction.response.send_message('done',ephemeral=True)
        await buttonR.queue_size_selected(interaction,self.answer)

          

class Maps_select_view(View):

    def __init__(self,client):
        super().__init__(timeout=None)
        self.client = client
        self.button = Button_clicked(self.client)
        self.channels_dict = Channels_dict()


    @discord.ui.select(options = [
        discord.SelectOption(label="Random",emoji= '❓',description="the bot selects a random map after filling the queue",default=True),
        discord.SelectOption(label="FACTORY"),
        discord.SelectOption(label="CUSTOMS"),
        discord.SelectOption(label="WOODS"),
        discord.SelectOption(label="INTERCHANGE"),
        discord.SelectOption(label="RESERVE"),
        discord.SelectOption(label="SHORELINE"),
        discord.SelectOption(label="THE LAB"),
        discord.SelectOption(label="LIGHTHOUSE")
        ])
    async def select_callback(self,interaction,select):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if (interaction.user.id != host):
            embed = discord.Embed(
            title=f"Only the host can select map",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        await self.button.selected(interaction,select)
        


class Squad_select_view(View):

    def __init__(self,client):
        super().__init__(timeout=None)
        self.client = client
        self.button = Button_clicked(self.client)
        self.channels_dict = Channels_dict()

    @discord.ui.select(options = [
        discord.SelectOption(label="1 man squad",default=True),
        discord.SelectOption(label="2 man squad",),
        discord.SelectOption(label="3 man squad",),
        discord.SelectOption(label="4 man squad",),
        discord.SelectOption(label="5 man squad",),
        
        ])
    async def select_callback(self,interaction,select):
        host = self.channels_dict.find_by_value(interaction.channel_id)
        if (interaction.user.id != host):
            embed = discord.Embed(
            title=f"Only the host can select squads",
            color = 0xff00)  
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        await self.button.squads_selected(interaction,select)



async def setup(client):    
    
    await client.add_cog(Button_clicked(client))
   
    