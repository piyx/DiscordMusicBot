from dataclasses import dataclass
import os

from ytmusicapi import YTMusic


@dataclass
class YTSong:
    url: str
    title: str
    duration: int
    thumbnail: str


class Youtube:
    def _get_yt_song(self, track: dict) -> YTSong | None:
        if track is None:
            return None

        return YTSong(
            url=f"https://www.youtube.com/watch?v={track['videoId']}",
            title=track["title"],
            duration=track["duration"],
            thumbnail=track["thumbnails"][-1]["url"],
        )

    def get_song_by_name(self, song_name: str) -> YTSong | None:
        results = YTMusic().search(song_name)
        categories = ["video", "song"]
        track = next(item for item in results if item["resultType"] in categories)
        return self._get_yt_song(track)

    def get_playlist_songs(self, playlist_id: str) -> list[YTSong]:
        results = YTMusic().get_playlist(playlistId=playlist_id)
        return [self._get_yt_song(track) for track in results["tracks"]]

    def download_song(self, yt_song: YTSong, download_location: str) -> None:
        os.system(f"yt-dlp -x --force-overwrites -o {download_location} {yt_song.url}")