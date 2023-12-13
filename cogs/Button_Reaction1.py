import time
import discord
from .db1 import DB1
from discord.ext import commands
import asyncio
from .queue1 import Queue1
from discord.ui import *
import Config
import random
from .singleton1 import *
import aiomysql






class Button_clicked(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.pics = Config.get_maps_pics()
        self.myDB = DB1(self.client)
        self.queue_dict = Queue_dict()
        self.channels_dict = Channels_dict()
        
       

    async def register_helper(self,interaction: discord.Interaction, player_username: str):
        await self.myDB.register(interaction,player_username)


    async def Register_clicked(self,interaction: discord.Interaction):
        
        person = interaction.user

        if not (await self.myDB.check_by_id(person)):

            embed = discord.Embed(
            title="you have already registered",
            color = 0xff0000)  
            await interaction.response.send_message(embed=embed,ephemeral=True) 
            return
        try:
            await interaction.response.send_modal(username_Modal())

        except:
            return

    async def change_username_helper(self,interaction: discord.Interaction, player_username: str):
        await self.myDB.change_username(interaction,player_username)
    async def Change_username_clicked(self,interaction):

        person = interaction.user
        if (await self.myDB.check_by_id(person)):

            embed = discord.Embed(
            title="You should register first",
            color = 0xffff00)
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        await interaction.response.send_modal(change_username_Modal())


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
            if(el_queue.is_full()):
                embed = discord.Embed(
                    title=f"The queue is full",
                    color=0x0000ff)
                await interaction.response.send_message(embed=embed, ephemeral=True)

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



    async def host_clicked(self, interaction: discord.Interaction):

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
        text_channel = await interaction.guild.create_text_channel(f'{interaction.user.display_name}', category=text_category)

        view = Host_Menu(self.client)
        embed = discord.Embed(
        title=f"5 man squad ",
        description="",
        color = 0xffffff)
        embed.set_author(name=interaction.user.display_name)
        embed.set_image(url='https://cdn.discordapp.com/attachments/487658114464612352/1008024714897260554/download.png')
        embed.set_thumbnail(url=interaction.user.display_avatar)
        msg = await text_channel.send(embed=embed, view = view)
        await msg.pin()



        host_set.add(interaction.user.id)
        my_queue = Queue1(self.client,interaction,text_channel,10,msg.id)

        voice_category = discord.utils.get(interaction.guild.categories, id= Config.get_custom_games_voice_id())
        voice_channel = await interaction.guild.create_voice_channel(f'{interaction.user.display_name}', category=voice_category)
        invite = await voice_channel.create_invite()
        await text_channel.send(invite)

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





    async def open_queue_clicked(interaction):
        pass

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
        await asyncio.sleep(5)
        counter = 0
        for i in voice_category.voice_channels:
            if i.name == interaction.user.display_name or interaction.user.display_name+ str(" Team 1") or interaction.user.display_name + str(" Team 2"):
                counter += 1
                await i.delete()
                if counter == 3:
                    break

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
        el_queue
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




    async def start_game(self,interaction):
        host_id = self.channels_dict.find_by_value(interaction.channel_id)
        host = await self.client.fetch_user(host_id)
        el_queue = self.queue_dict.get_queue(host_id)
        if el_queue.queue_size > len(el_queue.get_lst()):
            players = el_queue.get_lst()
        else:
            players = el_queue.get_lst()[:el_queue.queue_size]

        myDB = await aiomysql.connect(host='localhost',user='root',password='ayham123123',db='treydb')

        db_command = f"SELECT `username` FROM `players` WHERE player = '{players[0]}'"
        for i in players[1:]:
            db_command += f" or player = {i}"

        async with myDB.cursor() as cur:
            await cur.execute(db_command)
            await myDB.commit()
            in_game_names = await cur.fetchall()

        teams_players = [[], []]
        teams_strings = []
        if (el_queue.players_in_team > 1):
            for i in range(1,3):
                teams_strings.append(f'Team {i}\n')

            while (len(players) >0):

                for j in range(len(teams_strings)):
                    if(len(players) <= 0):
                        break

                    player = random.choice(el_queue.queue_lst)   #player's id
                    member = await interaction.guild.fetch_member(player)
                    teams_strings[j] = teams_strings[j] + str(member.mention)
                    teams_players[j].append(member)
                    players.remove(player)

        else:
            for i in el_queue.queue_lst:
                member = await self.client.fetch_user(i)
                teams_strings.append(member.mention)


        view = close_channel_button(self.client)

        embed = discord.Embed(
            title = f'Match started',
            description= f'{el_queue.players_in_team} man squad',
            color = discord.Colour.random())
        embed.set_author(name=host)
        if (el_queue.map == "RANDOM"):
            game_map = random.choice(Config.get_maps())
            el_queue.map = game_map
        embed.set_image(url=self.pics.get(el_queue.map))
        embed.set_thumbnail(url=host.display_avatar)
        for i in teams_strings:
            embed.add_field(name=' ㅤ\n',value= i)



        embed.add_field(name= 'EFT names', value= in_game_names,inline=True)
        embed.add_field(name= 'Game mode / limits: ', value=el_queue.game_mode,inline=False)

        msg = await interaction.channel.fetch_message(el_queue.msg_id)
        await msg.delete()
        await interaction.channel.send(embed=embed,view=view)


        voice_category = discord.utils.get(interaction.guild.categories, id=Config.get_custom_games_voice_id())
        voice_channel1 = await interaction.guild.create_voice_channel(f'{interaction.user.display_name} Team 1',category=voice_category)
        voice_channel2 = await interaction.guild.create_voice_channel(f'{interaction.user.display_name} Team 2',category=voice_category)
        voice_category = discord.utils.get(interaction.guild.categories, id=Config.get_custom_games_voice_id())
        for i in voice_category.voice_channels:
            if i.name == host.display_name:
                in_main_voice_channel = i.members
                break


        for member1 in teams_players[0]:
            if member1 in in_main_voice_channel:
                await member1.move_to(voice_channel1)


        for member2 in teams_players[1]:
            if member2 in in_main_voice_channel:
                await member2.move_to(voice_channel2)



        #TODO: fix players names
        #TODO: implement private session
















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
            description= f'',
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
        self.pre = False



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
        if interaction.user.id != host:
            embed = discord.Embed(
            title=f"Only the host can change squads",
            color = 0xff00)
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return
        squad_view = Squad_select_view(self.client)
        await interaction.channel.send(view = squad_view)


    # @discord.ui.button(label='Queue size' ,style=discord.ButtonStyle.blurple)
    # async def Select_Queue(self, interaction:discord.Interaction, button: discord.ui.Button):
    #     host = self.channels_dict.find_by_value(interaction.channel_id)
    #     if (interaction.user.id != host):
    #         embed = discord.Embed(
    #         title=f"Only the host can Queue size",
    #         color = 0xff00)
    #         await interaction.response.send_message(embed=embed,ephemeral=True)
    #         return
    #
    #     await interaction.response.send_modal(Queue_size_Modal())



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



    @discord.ui.button(label='Start Game', style=discord.ButtonStyle.success)
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        channels_dict = Channels_dict()
        host = channels_dict.find_by_value(interaction.channel.id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
            title=f"Only the host can start the game",
            color = 0xff00)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        await self.button.start_game(interaction)

    @discord.ui.button(label='Close Channel', style=discord.ButtonStyle.grey)
    async def Close_channel1(self, interaction: discord.Interaction, button: discord.ui.Button):
        channels_dict = Channels_dict()
        host = channels_dict.find_by_value(interaction.channel.id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
                title=f"Only the host can close the channel",
                color=0xff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.button.Close_Channel_clicked(interaction)



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
        elif int(self.answer.value) <1:
            await interaction.response.send_message('please enter positive number above 0', ephemeral= True)
            return

        await interaction.response.send_message('done',ephemeral=True)
        await buttonR.queue_size_selected(interaction,self.answer)

class username_Modal(discord.ui.Modal,title= 'Tarkov Bot'):

    answer = discord.ui.TextInput(label='Enter your username',style=discord.TextStyle.short,placeholder="Tarkov's username",required= True,max_length=15)
    async def on_submit(self,interaction: discord.Interaction):
        buttonR = Button_clicked(interaction.client)
        await buttonR.register_helper(interaction,str(self.answer))


class change_username_Modal(discord.ui.Modal,title= 'Tarkov Bot'):

    answer = discord.ui.TextInput(label='Enter your username',style=discord.TextStyle.short,placeholder="Tarkov's username",required= True,max_length=15)
    async def on_submit(self,interaction: discord.Interaction):
        buttonR = Button_clicked(interaction.client)
        await buttonR.change_username_helper(interaction,str(self.answer))




class close_channel_button(discord.ui.View):
    def __init__(self,client):
        super().__init__()
        self.client = client
        self.button = Button_clicked(self.client)
    @discord.ui.button(label='Close Channel', style=discord.ButtonStyle.grey)
    async def Close_channel1(self, interaction: discord.Interaction, button: discord.ui.Button):
        channels_dict = Channels_dict()
        host = channels_dict.find_by_value(interaction.channel.id)
        if str(host) != str(interaction.user.id):
            embed = discord.Embed(
                title=f"Only the host can close the channel",
                color=0xff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.button.Close_Channel_clicked(interaction)


class Maps_select_view(View):

    def __init__(self,client):
        super().__init__(timeout=None)
        self.client = client
        self.button = Button_clicked(self.client)
        self.channels_dict = Channels_dict()


    @discord.ui.select(options = [
        discord.SelectOption(label="RANDOM",emoji= '❓',description="the bot selects a random map after filling the queue"),
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
        discord.SelectOption(label="1 man squad"),
        discord.SelectOption(label="2 man squad"),
        discord.SelectOption(label="3 man squad"),
        discord.SelectOption(label="4 man squad"),
        discord.SelectOption(label="5 man squad"),

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

