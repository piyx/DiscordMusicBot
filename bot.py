import os


from discord.ext import commands
from discord import Embed
from discord import Colour
from dotenv import load_dotenv


load_dotenv(".env")
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix=".")


@bot.event
async def on_ready():
    print(f"Bot Ready! Logged in as {bot.user}")
    print("-----------------------------------")


@bot.command()
async def ping(ctx):
    """Displays the bot ping"""
    embed = Embed(title=f"Pong! {round(bot.latency*1000)}ms", color=Colour.blue())
    await ctx.send(embed=embed)


@bot.command()
async def delete(ctx, amount=2):
    """Deletes <amount> number of messages"""
    await ctx.channel.purge(limit=amount)


bot.load_extension(f"music")  # load all commands from music.py
bot.run(TOKEN)