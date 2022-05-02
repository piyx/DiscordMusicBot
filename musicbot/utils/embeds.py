from gettext import ngettext
from itertools import islice
from collections import deque

from discord import Color
from discord import Embed

from musicbot.utils.youtube import YTSong


def now_playing_embed(ctx, yt_song: YTSong) -> Embed:
    embed = Embed(
        title=yt_song.title,
        url=yt_song.url,
        description=f"`Duration: {yt_song.duration}`",
        color=Color.magenta(),
        inline=True
    )

    embed.set_thumbnail(url=yt_song.thumbnail)
    embed.set_author(name="Now Playing", icon_url=ctx.author.avatar_url)
    return embed

def queue_embed(ctx, now_playing: YTSong, queue: deque[YTSong]) -> Embed:
    queue_size = len(queue)
    embed = Embed(
        title=now_playing.title,
        url=now_playing.url,
        description=f"`Being played. Duration: {now_playing.duration}`\n",
        inline=True,
        color=Color.dark_green()
    )

    for position, yt_song in enumerate(islice(queue, 5), 1):
        embed.add_field(
            name=u'\u200b', # It represents empty value
            value=f"`{position}.` [{yt_song.title}]({yt_song.url})\n `Duration: {yt_song.duration}`",
            inline=False
        )

    embed.set_author(
        name=f"{queue_size} {ngettext('song', 'songs', queue_size)} queued",
        icon_url=ctx.author.avatar_url
    )
    
    embed.set_thumbnail(url=now_playing.thumbnail)
    return embed