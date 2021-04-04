import re
from ytmusicapi import YTMusic
from datetime import timedelta
from dataclasses import dataclass
from urllib.request import urlopen
from typing import Optional, Iterator


@dataclass
class YTSong:
    vidurl: str
    title: str
    duration: str
    thumbnail: str


class Youtube:
    def __init__(self):
        self.ytmusic = YTMusic()

    def _get_video_id(self, song_name: str) -> Optional[str]:
        '''Extracts the video_id of the first video from youtube search result for the given song name'''
        query = "+".join(song_name.split())
        search_url = f"https://www.youtube.com/results?search_query={query}"
        html = urlopen(search_url).read().decode()
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        return video_ids[0] if video_ids else None

    def _get_ytsong(self, track: dict) -> YTSong:
        '''Extract useful information from results data and return list of YTSongs'''
        vid_id = track['videoId']
        return YTSong(vidurl=f"https://www.youtube.com/watch?v={vid_id}",
                      title=track['title'],
                      duration=track['duration'] if "duration" in track else str(
                          timedelta(seconds=int(track['lengthSeconds']))),
                      thumbnail=f"https://i.ytimg.com/vi/{vid_id}/sddefault.jpg")

    def get_song_by_name(self, song_name: str) -> Optional[YTSong]:
        '''Get YTsong for the given song name'''
        video_id = self._get_video_id(song_name)
        result = self.ytmusic.get_song(video_id)
        if 'status' in result and result['status'] == ['fail']:
            return None

        return self._get_ytsong(result)

    def get_songs_from_playlist(self, playlist_id: str) -> Optional[Iterator[YTSong]]:
        '''Get iterator of YTSongs from given playlist id'''
        try:
            results = self.ytmusic.get_playlist(playlist_id)
        except Exception:
            return None

        return [self._get_ytsong(track) for track in results['tracks']]
