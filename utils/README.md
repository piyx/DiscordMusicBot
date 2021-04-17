# DiscordAnimeBot

Discord bot which uses a very simple API to get basic useful information about anime including download links


## Usage

```python
from animeAPI import get_anime_info

>>> get_anime_info('Naruto') 
AnimeInfo(title='Naruto Shippuden (Season 1-21 + Naruto + Movies + OVAs) 1080p Dual Audio HEVC', 
          genres='Action, Adventure, Comedy, Super Power, Martial Arts, Shounen', 
          episodes='(Seasons 1-21 + Movies + OVAs)', 
          rating='PG-13 – Teens 13 or older', 
          duration='23 min. per ep.', 
          aired='Unknown', 
          thumbnail='a-very-long-url', 
          download='long-url'
        )

>>> get_anime_info('Handa kun') 
AnimeInfo(title='Handa-Kun (Season 1) 1080p Dual Audio HEVC', 
          genres='Slice of Life, Comedy, Shounen', 
          episodes='12', 
          rating='PG-13 – Teens 13 or older', 
          duration='24 min. per ep.', 
          aired='Jul 8, 2016 to Sep 23, 2016', 
          thumbnail='a-very-long-url', 
          download='long-url'
        )
```
