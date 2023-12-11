import discord
from discord.ext import commands, tasks
import Config
from discord import app_commands
from .Button_Reaction1 import Button_clicked


class Init(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='init', description='initializing the Bot')
    async def init(self, ctx: commands.Context):
        # Ayham's ID
        if ctx.message.author.id != 359079983777447937:
            await ctx.defer(ephemeral=True)
            await ctx.reply("You are not allowed to use this command")
            return

        channel_id = Config.get_register_channel()
        channel = ctx.guild.get_channel(int(channel_id))
        embed = discord.Embed(
            title="Welcome to custom games bot",
            description="make sure you register before you queue",
            color=0x00ff00
        )

        view = Register_Menu(self.client)
        # await channel.send(embed=embed, view=view)

        channel_id = Config.get_create_lobby_channel()
        channel1 = ctx.guild.get_channel(int(channel_id))
        embed1 = discord.Embed(
            title="Create lobby",
            description=f"Click Host to create you're own text and voice channels\nif you can't host make sure you register",
            color=0x00ffff
        )

        view1 = Create_lobby_Menu(self.client)
        # await channel1.send(embed=embed1, view=view1)
        await ctx.defer(ephemeral=True)
        await ctx.reply("done!")


class Create_lobby_Menu(commands.Cog):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.button = Button_clicked(self.client)
        self.value = None



    # @discord.ui.button(label='Host', style=discord.ButtonStyle.green, custom_id="Host")
    @app_commands.command(name='host', description='Host your game')
    async def Host(self, interaction: discord.Interaction):
        await self.button.host_clicked(interaction)


class Register_Menu(commands.Cog):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.button = Button_clicked(self.client)
        self.value = None


    @app_commands.command(name='register', description='register your account with TarkovBot')
    async def register(self, interaction: discord.Interaction):
        await self.button.Register_clicked(interaction)

    @app_commands.command(name='change_username', description='change your username')
    async def Change_username(self, interaction: discord.Interaction):
        await self.button.Change_username_clicked(interaction)





async def setup(client):
    await client.add_cog(Init(client))
    await client.add_cog(Create_lobby_Menu(client))
    await client.add_cog(Register_Menu(client))


