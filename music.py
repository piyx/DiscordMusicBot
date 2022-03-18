from collections import deque
from itertools import islice
from gettext import ngettext
import contextlib
import os

from discord.ext import commands
from discord import FFmpegOpusAudio

from youtube import YTSong, Youtube
from messages import beautify_message
from messages import Emoji
from embeds import now_playing_embed
from embeds import queue_embed


MEDIA_FOLDER = "songs"
MUSIC_NAME = "song.opus"


class MusicPlayer:
    def __init__(self, voice_client, server_id: int) -> None:
        self.voice_client = voice_client
        self.now_playing = None
        self.queue = deque()
        self.server_id = server_id
        self.file_path = f"{MEDIA_FOLDER}/{server_id}_{MUSIC_NAME}"
    
    def is_running(self):
        return self.voice_client.is_playing() or self.voice_client.is_paused()


class MusicCommands(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.youtube = Youtube()
        self.music_players = {}
    
    def get_music_player(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            return self.music_players[server_id]

        music_player = MusicPlayer(voice_client=ctx.voice_client, server_id=server_id)
        self.music_players[server_id] = music_player
        return music_player

    def download_and_play(self, music_player: MusicPlayer) -> None:
        music_player.now_playing = music_player.queue.popleft()
            
        self.youtube.download_song(
            yt_song=music_player.now_playing, 
            download_location=music_player.file_path
        )
        
        music_player.voice_client.play(
            FFmpegOpusAudio(music_player.file_path),
            after=lambda x: self.check_queue(music_player)
        )

    def check_queue(self, music_player: MusicPlayer) -> None:
        if music_player.queue:
            self.download_and_play(music_player)
            return

        # If queue is empty, cleanup and delete
        music_player.now_playing = None
        with contextlib.suppress(FileNotFoundError):
            os.remove(music_player.file_path)
        del self.music_players[music_player.server_id]
    
    @commands.command()
    async def play(self, ctx, *, song_name: str) -> None:
        '''Searches the song on youtube and plays the first search result'''
        try:
            yt_song = self.youtube.get_song_by_name(song_name)
        except Exception as e:
            print(e)
            await ctx.send(beautify_message(Emoji.Error, 'Error playing song!'))
        
        await self.play_music(ctx, deque([yt_song]))
    
    @commands.command()
    async def ytplaylist(self, ctx, playlist_id: str) -> None:
        '''Get all songs from the playlist and add to queue'''
        try:
            yt_songs = self.youtube.get_playlist_songs(playlist_id=playlist_id)
        except Exception as e:
            print(e)
            await ctx.send(beautify_message(Emoji.Error, "Invalid playlist or error fetching songs."))
        
        await self.play_music(ctx, deque(yt_songs))
        await ctx.send(beautify_message(Emoji.Check, f"{len(yt_songs)-1} songs queued."))
    
    async def play_music(self, ctx, yt_songs: deque[YTSong]) -> None:
        music_player = self.get_music_player(ctx)
        music_player.queue += yt_songs

        if music_player.is_running():
            n_songs = ngettext("Song", "Songs", len(yt_songs))
            return await ctx.send(beautify_message(Emoji.Check, f"{n_songs} added to queue."))
        
        async with ctx.typing():
            self.download_and_play(music_player)
            return await ctx.send(embed=now_playing_embed(ctx, music_player.now_playing))
    
    @play.before_invoke
    @ytplaylist.before_invoke
    async def ensure_voice(self, ctx):
        '''Ensure user is connected to voice channel'''
        if ctx.voice_client:
            return
        
        if ctx.author.voice:
            return await ctx.author.voice.channel.connect()
        
        await ctx.send(beautify_message(Emoji.Error, "You are not connected to voice channel."))
        raise commands.CommandError("User not connected to voice channel.")

    @commands.command()
    async def now_playing(self, ctx) -> None:
        '''Displays the now playing song'''
        music_player = self.get_music_player(ctx)
        print(ctx.guild.id)
        print(self.music_players)
        print(music_player.now_playing, "okay")
        await ctx.send(embed=now_playing_embed(
            ctx=ctx, 
            yt_song=music_player.now_playing)
        )
    
    @commands.command()
    async def queue(self, ctx) -> None:
        '''Displays the songs queue'''
        music_player = self.get_music_player(ctx)
        await ctx.send(embed=queue_embed(
            ctx=ctx, 
            now_playing=music_player.now_playing, 
            queue=music_player.queue)
        )

    @commands.command()
    async def clear(self, ctx) -> None:
        '''Clear the song queue'''
        music_player = self.get_music_player(ctx)
        music_player.queue.clear()
        await ctx.send(beautify_message(Emoji.Check, "Queue cleared."))
    
    @commands.command()
    async def pause(self, ctx) -> None:
        '''Pause the current playing song'''
        music_player = self.get_music_player(ctx)
        music_player.voice_client.pause()
        await ctx.send(beautify_message(Emoji.Pause, "Music paused."))
    
    @commands.command()
    async def resume(self, ctx) -> None:
        '''Resume the current playing song'''
        music_player = self.get_music_player(ctx)
        if music_player.voice_client.is_paused():
            music_player.voice_client.resume()
        
        await ctx.send(beautify_message(Emoji.Resume, "Music resumed."))

    @commands.command()
    async def stop(self, ctx) -> None:
        '''Stop playing music, clear queue, disconnect bot and delete music player'''
        music_player = self.get_music_player(ctx)
        music_player.queue.clear()
        music_player.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send(beautify_message(Emoji.Stop, "Music stopped"))
    
    @commands.command()
    async def skip(self, ctx, n_songs: int = 1) -> None:
        '''Skip <n_songs> from the queue'''
        music_player = self.get_music_player(ctx)
        queue = music_player.queue
        n_skip = min(len(queue)+1, max(1, n_songs))
        
        for _ in range(n_skip-1):
            queue.popleft()
        
        music_player.voice_client.stop()
        return await ctx.send(beautify_message(Emoji.Check, f"{n_skip} {ngettext('Song', 'Songs', n_skip)} skipped"))


    @commands.command()
    async def repeat(self, ctx, times: int=1) -> None:
        '''Repeat the current playing song <times> times'''
        music_player = self.get_music_player(ctx)
        for _ in range(min(times, 10)):
            music_player.queue.appendleft(music_player.now_playing)
        
        await ctx.send(beautify_message(Emoji.Success, f"Song will repeat for {min(times, 10)} times."))
    
    @pause.before_invoke
    @resume.before_invoke
    @stop.before_invoke
    @repeat.before_invoke
    @skip.before_invoke
    @clear.before_invoke
    @now_playing.before_invoke
    @queue.before_invoke
    async def ensure_song_playing(self, ctx) -> None:
        server_id = ctx.guild.id
        music_player = self.music_players.get(server_id, None)
        if music_player and music_player.is_running():
            return
        
        await ctx.send(beautify_message(Emoji.Error, "No music is being played."))
        raise commands.CommandError("No Music is being played")


def setup(bot_client):
    bot_client.add_cog(MusicCommands(bot_client))