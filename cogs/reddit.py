from discord import Embed
from discord import Color
from discord.ext import commands


from utils.reddit import get_reddit_post


class Posts(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def reddit(self, ctx, subreddit: str, category: str = "hot"):
        '''Displays one post from the subreddit based on category'''
        post = get_reddit_post(subreddit, category)

        if isinstance(post, str): # Error message in str
            embed = Embed(title=post, color=Color.random())
            return await ctx.send(embed=embed)
        
        embed = Embed(title=f"{post.name}\n{post.title}", 
                      description=f"{post.desc}\n{post.url}", 
                      color=Color.random()
                    )

        embed.set_image(url=post.url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Posts(client))
