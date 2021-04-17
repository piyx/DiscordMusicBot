from discord import Embed
from discord import Color
from discord.ext import commands


from utils.animeAPI import get_anime_info


class Anime(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    
    @commands.command()
    async def anime(self, ctx, *, anime_name):
        '''Get download links and useful information for the given anime'''
        async with ctx.typing():
            anime = get_anime_info(query=anime_name)
            if anime is None:
                embed = Embed(description=f"Coudn't find **{anime_name}**",
                              color=Color.dark_green())
                return await ctx.send(embed=embed)

            embed = Embed(color=Color.dark_green())
            embed.set_author(name=anime.title, icon_url=ctx.author.avatar_url)
            embed.add_field(name='Episodes', value=anime.episodes, inline=False)
            embed.add_field(name='Duration', value=anime.duration, inline=False)
            embed.add_field(name='Genres', value=anime.genres, inline=False)
            embed.add_field(name='Rating', value=anime.rating, inline=False)
            embed.add_field(name='Aired', value=anime.aired, inline=False)
            
            embed.add_field(name="Link", 
                            value=f"**[Download anime from here]({anime.download})**", 
                            inline=False
                        )
            
            embed.set_image(url=anime.thumbnail)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Anime(client))