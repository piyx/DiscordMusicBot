import os
import shutil
import discord
from discord.utils import get
from collections import deque
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio
from collections import defaultdict


from utils.messages import message
from utils.youtube import Youtube, YTSong
from utils.embeds import np_embed, q_embed


ytdl_format_options = {
    'format': 'bestaudio/best',
    'forceipv4': True,
    'cookies': True
}

MEDIA_PATH = "./media"
MUSIC_NAME = "song.m4a"
ytdl = YoutubeDL(ytdl_format_options)


class NoMusicPlayingException(Exception):
    pass


class NotInVoiceChannelException(Exception):
    pass


class MusicPlayer:
    def __init__(self, voice, current: YTSong, server: int):
        self.voice = voice
        self.current = current
        self.queue = deque([])
        self.media_folder = f"{MEDIA_PATH}/{server}/"


class Music(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.youtube = Youtube()
        self.music_players = {}

    @commands.command()
    async def play(self, ctx, *, song_name: str) -> None:
        '''Searches the song on youtube and plays the song'''
        ytsong = self.youtube.get_song_by_name(song_name)
        if ytsong is None:
            return await ctx.send(message("ERROR", "Song could not be found"))

        await self.play_music(ctx, deque([ytsong]))

    @commands.command()
    async def ytplaylist(self, ctx, playlist_id: str) -> None:
        '''Gets list of all songs from playlist and adds it to queue'''
        ytsongs = self.youtube.get_songs_from_playlist(playlist_id)
        if ytsongs is None:
            return await ctx.send(message("ERROR", "Invalid playlist or playlist is private"))

        await ctx.send(message("CHECK", "Adding songs to queue"))
        await self.play_music(ctx, deque(ytsongs), musictype="YTPLAYLIST")

    def download(self, server: int) -> bool:
        # Remove existing songs
        player = self.music_players[server]
        media_folder = player.media_folder

        for item in os.listdir(media_folder):
            os.remove(media_folder+item)

        # Download song to respective folder
        ytdl_format_options['outtmpl'] = media_folder + MUSIC_NAME

        try:
            with YoutubeDL(ytdl_format_options) as ydl:
                ydl.download([player.current.vidurl])
                return True
        except Exception as e:
            print(e)
            return False

    def check_queue(self, server: int) -> None:
        player = self.music_players[server]
        voice = player.voice
        music_path = player.media_folder + MUSIC_NAME

        # If queue is empty, delete respective folder and the player
        if not player.queue:
            player.current = None
            shutil.rmtree(player.media_folder)
            del self.music_players[server]
            return

        # If queue is not empty, remove song and download next
        os.remove(music_path)
        player.current = player.queue.popleft()
        self.download(server)
        voice.play(FFmpegPCMAudio(music_path),
                   after=lambda x: self.check_queue(server))

        voice.source = discord.PCMVolumeTransformer(voice.source, volume=1.0)

    async def play_music(self, ctx, ytsongs: deque[YTSong], musictype=None) -> None:
        server = ctx.guild.id
        voice = get(self.bot_client.voice_clients, guild=ctx.guild)

        if server not in self.music_players:
            self.music_players[server] = MusicPlayer(
                voice, ytsongs.popleft(), server)

        player = self.music_players[server]
        music_path = player.media_folder + MUSIC_NAME
        os.makedirs(player.media_folder, exist_ok=True)

        # If not song is being played, download next and play it
        if not voice.is_playing() and not voice.is_paused():
            async with ctx.typing():
                status = self.download(server)
                if not status:
                    return await ctx.send(message("ERROR", "Song cannot be streamed"))

                voice.play(FFmpegPCMAudio(music_path),
                           after=lambda x: self.check_queue(server))

                voice.source = discord.PCMVolumeTransformer(
                    voice.source, volume=1.0)

            await ctx.send(embed=np_embed(ctx, player.current))

        # This check avoids sending message N times, since playlist contains N songs
        if musictype not in ['YTPLAYLIST'] and len(ytsongs) == 1:
            await ctx.send(message("CHECK", "Song added to queue"))

        player.queue += ytsongs

    @play.before_invoke
    @ytplaylist.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client:
            return

        if ctx.author.voice:
            return await ctx.author.voice.channel.connect()

        await ctx.send(message("ERROR", "You are not connected to a voice channel"))
        raise NotInVoiceChannelException("User Not connected to voice channel")

    @commands.command()
    async def pause(self, ctx):
        '''Pauses the current playing song'''
        player = self.music_players.get(ctx.guild.id, None)
        player.voice.pause()
        await ctx.send(message("PAUSE", "Music paused"))

    @commands.command()
    async def resume(self, ctx):
        '''Resume the current paused song'''
        player = self.music_players.get(ctx.guild.id, None)
        if player.voice.is_paused():
            player.voice.resume()
            return await ctx.send(message("RESUME", "Music resumed"))

        await ctx.send(message("CHECK", "Song is already being played"))

    @commands.command()
    async def stop(self, ctx):
        '''Stops the player, clears queue and disconnects voice channel'''
        player = self.music_players.get(ctx.guild.id, None)
        player.queue.clear()
        player.voice.stop()
        await ctx.voice_client.disconnect()
        await ctx.send(message("STOP", "Music stopped"))

    @commands.command()
    async def np(self, ctx):
        '''Displays the now playing song info'''
        player = self.music_players.get(ctx.guild.id, None)
        await ctx.send(embed=np_embed(ctx, player.current))

    @commands.command()
    async def queue(self, ctx):
        '''Displays the song queue'''
        player = self.music_players.get(ctx.guild.id, None)
        await ctx.send(embed=q_embed(ctx, player.current, player.queue))

    @commands.command()
    async def clear(self, ctx):
        '''Clears the queue'''
        player = self.music_players.get(ctx.guild.id, None)
        player.queue.clear()
        await ctx.send(message("CHECK", "Queue cleared"))

    @commands.command()
    async def volume(self, ctx, volume: int):
        '''Sets the volume'''
        player = self.music_players.get(ctx.guild.id, None)
        if not (0 <= volume <= 100):
            return await ctx.send(message("ERROR", "Volume should in range [0,100]"))

        player.voice.source.volume = volume/100
        await ctx.send(message("CHECK", f"Volume set to {volume}"))

    @commands.command()
    async def skip(self, ctx):
        '''Skips the current song'''
        player = self.music_players.get(ctx.guild.id, None)
        player.voice.stop()
        await ctx.send(message("CHECK", "Music skipped"))

    @commands.command()
    async def repeat(self, ctx, times: int = 1):
        '''Repeats the current playing song'''
        player = self.music_players.get(ctx.guild.id, None)
        for _ in range(times):
            player.queue.appendleft(player.current)

        await ctx.send(message("SUCCESS", f"Song will repeat for {times} times"))

    @pause.before_invoke
    @resume.before_invoke
    @stop.before_invoke
    @repeat.before_invoke
    @skip.before_invoke
    @volume.before_invoke
    @clear.before_invoke
    @np.before_invoke
    @queue.before_invoke
    async def ensure_song_playing(self, ctx):
        player = self.music_players.get(ctx.guild.id, None)
        if player and (player.voice.is_paused() or player.voice.is_playing()):
            return

        await ctx.send(message("ERROR", "No music is being played"))
        raise NoMusicPlayingException("No music is being played")


def setup(bot_client):
    bot_client.add_cog(Music(bot_client))
