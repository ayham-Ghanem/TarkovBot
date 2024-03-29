from ast import Num
from dis import disco
import imp
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
from discord.ui import *
import Config
from .singleton1 import Channels_dict, Queue_dict


class Queue1():

    def __init__(self, client, interaction: discord.Interaction, new_channel, queue_size, msg_id):
        self.client = client
        self.maps = Config.get_maps()
        self.pics = Config.get_maps_pics()
        self.queue_size = queue_size
        self.host_id = interaction.user.id
        self.players_in_team = 5
        self.msg_id = msg_id
        self.game_mode = 'No Limits'
        self.queue_lst = []
        self.map = "RANDOM"
        q_dict = Queue_dict()
        channels_dict = Channels_dict()
        q_dict.add(interaction.user.id, self)
        channels_dict.add(interaction.user.id, new_channel.id)

    def get_lst(self):
        return self.queue_lst

    def is_full(self):
        return len(self.queue_lst) >= self.queue_size

    def change_players_in_team(self, num):
        self.players_in_team = int(num)
        self.queue_size = self.players_in_team*2

    def change_map(self, map):
        self.map = map

    def change_queue_size(self, num):
        self.queue_size = num

    def check_in_lst(self, user):
        return user.id in self.queue_lst

    def start_Check(self):
        return len(self.queue_lst) >= self.queue_size

    def lst_join(self, user):
        self.queue_lst.append(user.id)

    def lst_leave(self, user):
        if self.check_in_lst(user):
            self.queue_lst.remove(user.id)





# async def setup(client):

#     await client.add_cog(Queue1(client))
