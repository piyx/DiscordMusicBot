import requests
from typing import Optional
from bs4 import BeautifulSoup
from dataclasses import dataclass, field


@dataclass
class AnimeInfo:
    title: str      = 'Unknown'
    genres: str     = 'Unknown'
    episodes: str   = 'Unknown'
    rating: str     = 'Unkwown'
    duration: str   = 'Unknown'
    aired: str      = 'Unknown'
    thumbnail: str  = 'Unknown'
    download: str   = 'Unknown'


def get_anime_info(query: str) -> Optional[AnimeInfo]:
    ''' Get information about an anime including download links if available

    Examples:
    
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
    '''
    url = f"https://kayoanime.com/?s={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select('#posts-container > li')

    if not results:
        return None

    anime_info = AnimeInfo()

    post = results[0]
    head = post.select_one('div.post-details > h2 > a')
    link, title = head.get('href'), head.text
    imgurl = post.find('img').get('src')

    anime_info = AnimeInfo()

    anime_info.title = title
    anime_info.download = link
    anime_info.thumbnail = imgurl


    # Get more details
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    post = soup.select_one('#the-post')
    if not post:
        return None

    info_div = []

    for div in post.select('div.toggle.tie-sc-open'):
        head = div.select_one('h3.toggle-head').text
        if head.startswith("Information"):
            info_div = div
    
    items = info_div.select('div.toggle-content > ul > li') if info_div else []
    for item in items:
        key, value = item.text.split(': ')
        key = key.lower()
        if key in anime_info.__dict__:
            setattr(anime_info, key, value)
    
    return anime_info