from .yt import YTSong
from discord import Color
from discord import Embed
from gettext import ngettext
from itertools import islice
from collections import deque


def np_embed(ctx, info: YTSong):
    '''Embed for now playing'''
    embed = Embed(title=f"{info.title}",
                  url=f"{info.vidurl}",
                  description=f"`Duration: {info.duration}`",
                  color=Color.magenta(),
                  inline=True
                  )
    embed.set_thumbnail(url=info.thumbnail)
    embed.set_author(
        name=f"Now playing", icon_url=ctx.author.avatar_url)
    return embed


def q_embed(ctx, info: YTSong, queue: deque[YTSong]):
    '''Embed for queued songs'''
    n = len(queue)
    embed = Embed(title=f"{info.title}",
                  url=f"{info.vidurl}",
                  description=f"`Being played. Duration: {info.duration}`\n",
                  inline=True,
                  color=Color.dark_green()
                  )
    embed.set_author(
        name=f"{n} {ngettext('song', 'songs', n)} queued",
        icon_url=ctx.author.avatar_url
    )

    first_ten = list(islice(queue, 5))
    for i, song in enumerate(first_ten, 1):
        embed.add_field(name=u'\u200b',
                        value=f"`{i}.` [{song.title}]({song.vidurl})\n `Duration: {song.duration}`",
                        inline=False
                        )

    embed.set_thumbnail(url=info.thumbnail)
    return embed
