import discord
from discord.ext import tasks
from discord.utils import get
from discord.ext import commands


from utils.messages import message


class Discord(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.status = "1 DVS BSTD"

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(self.status)
        )
        print("Bot is ready!")

    @commands.command()
    async def ping(self, ctx):
        '''Displays the ping'''
        embed = discord.Embed(
            title=f'Pong! {round(self.client.latency*1000)}ms', color=0x457832)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the best server lol.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has rage quit.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, amount=5):
        '''Deletes N number of messages'''
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def join(self, ctx):
        '''Joins the channel of author'''
        if not ctx.author.voice:
            return await ctx.send(message("ERROR", "You need to be in a voice channel"))

        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client

        if voice_client:
            await ctx.send(message("CHECK", "Already in a voice channel"))
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        await ctx.send(message("SUCCESS", f"Joined {channel}"))

    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        '''Leaves the current voice channel'''
        voice_client = ctx.voice_client
        if not voice_client:  # Check if bot instance is connected to voice channel
            await ctx.send(message("CHECK", f"Not in any channel"))
        else:
            await ctx.send(message("CHECK", f"Left {voice_client.channel}"))
            await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(Discord(client))
