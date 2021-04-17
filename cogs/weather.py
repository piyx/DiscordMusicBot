from discord import Color
from discord import Embed
from discord.ext import commands


from utils.weather import current_weather, astronomy, apod


class Sky(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command(aliases=['current', 'weth'])
    async def weather(self, ctx, city):
        '''Displays the city's weather'''
        weather = current_weather(city=city)

        if weather is None:
            embed = Embed(title=f"{city} is not a city lol!", color=Color.dark_teal())
            return await ctx.send(embed=embed)

        embed = Embed(title=weather.loc, color=Color.dark_green())
        embed.set_thumbnail(url=weather.icon)
        embed.add_field(name="Weather", value=weather.desc, inline=False)
        embed.add_field(name="Current", value=weather.curr, inline=False)
        embed.add_field(name="Feels Like", value=weather.feels, inline=False)
        embed.add_field(name="Wind Speed", value=weather.wind, inline=False)
        embed.add_field(name="Pressure", value=weather.pressure, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['astronomy', 'sun', 'moon'])
    async def astro(self, ctx, city):
        '''Displays the city's astronomy information'''
        astro = astronomy(city)

        if astro is None:
            embed = Embed(title=f"{city} is not a city lol!", color=Color.dark_teal())
            return await ctx.send(embed=embed)

        embed = Embed(title=f"Astronomy in {city}", color=Color.dark_green())
        embed.add_field(name="Sunrise", value=astro.sunrise, inline=False)
        embed.add_field(name="Sunset", value=astro.sunset, inline=False)
        embed.add_field(name="Moonrise", value=astro.moonrise, inline=False)
        embed.add_field(name="Moonset", value=astro.moonset, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['space', 'apod'])
    async def nasa(self, ctx):
        '''Displays astronomy picture of the day'''
        imgurl = apod()
        if imgurl is None:
            embed = Embed(title=f"Error fetching the image", color=Color.darker_grey())
            return await ctx.send(embed=embed)
        
        embed = Embed(title=f"Astronomy picture of day", color=Color.blurple())
        embed.set_image(url=imgurl)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Sky(client))