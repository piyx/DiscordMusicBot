from discord import Color
from discord import Embed
from gettext import ngettext
from itertools import islice
from collections import deque

from .youtube import YTSong


def np_embed(ctx, song: YTSong) -> Embed:
    '''Embed for now playing'''
    embed = Embed(title=f"{song.title}",
                  url=f"{song.vidurl}",
                  description=f"`Duration: {song.duration}`",
                  color=Color.magenta(),
                  inline=True
                  )
    
    embed.set_thumbnail(url=song.thumbnail)
    embed.set_author(name=f"Now playing", icon_url=ctx.author.avatar_url)
    return embed


def q_embed(ctx, current: YTSong, queue: deque[YTSong]) -> Embed:
    '''Embed for queued songs'''
    n = len(queue)
    embed = Embed(title=f"{current.title}",
                  url=f"{current.vidurl}",
                  description=f"`Being played. Duration: {current.duration}`\n",
                  inline=True,
                  color=Color.dark_green()
                  )
    
    embed.set_author(
        name=f"{n} {ngettext('song', 'songs', n)} queued",
        icon_url=ctx.author.avatar_url
    )

    for i, song in enumerate(islice(queue, 5), 1):
        embed.add_field(name=u'\u200b',
                        value=f"`{i}.` [{song.title}]({song.vidurl})\n `Duration: {song.duration}`",
                        inline=False
                       )

    embed.set_thumbnail(url=current.thumbnail)
    return embed