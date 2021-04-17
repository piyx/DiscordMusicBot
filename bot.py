import os
from discord.utils import get
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio


from utils.messages import message
from utils.credentials import TOKEN

# Discord token
token = TOKEN
bot = commands.Bot(command_prefix='.')


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(message("SUCCESS", f"cogs.{extension} has been loaded"))
    except Exception as e:
        await ctx.send(message("ERROR", e))


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(message("SUCCESS", f"cogs.{extension} has been unloaded"))
    except Exception as e:
        await ctx.send(message("ERROR", e))


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(message("SUCCESS", f"cogs.{extension} has been reloaded"))
    except Exception as e:
        await ctx.send(message("ERROR", e))


# Load all cog files
for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(message("ERROR", "Argument missing. Type .help <command> for usage details"))

bot.run(token)
