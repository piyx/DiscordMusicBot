# MusicBot

A minimal discord music bot with useful features.

## Setup

1. Go to https://discord.com/developers/applications and create an application.
2. Get the discord token and place it inside .env file
3. Install ffmpeg https://ffmpeg.org/download.html#build-windows or https://github.com/BtbN/FFmpeg-Builds/releases
4. Add ffmpeg to PATH.

## How to run
```
git clone https://github.com/piyx/DiscordMusicBot.git
cd DiscordMusicBot
pip install -r requirements.txt
pip install -e .
python musicbot/bot.py
```

## Bot commands

```
Bot prefix is . (dot)
To use any command prefix it with .
```

## Discord

| Command            | Description                  |
| :----------------- | :--------------------------- |
| .delete [amount=5] | deletes messages (default=5) |
| .ping              | displays the ping            |

## Music

| Command                   | Description                       |
| :------------------------ | :-------------------------------- |
| .play [music_name]        | plays the song from youtube       |
| .pause                    | pauses the current playing song   |
| .resume                   | resumes the song                  |
| .stop                     | stops playing music               |
| .now_playing              | displays the now playing song     |
| .queue                    | displays the song queue list      |
| .skip [n_songs=1]         | skips <n_songs> in the queue      |
| .clear                    | clears the queue                  |
| .repeat [times]           | repeats the current music n times |
| .ytplaylist [playlist_id] | Adds yt playlist songs to queue   |
