import praw
from typing import Union
from dataclasses import dataclass


from .credentials import CLIENT_ID
from .credentials import CLIENT_SECRET
from .credentials import USER_AGENT


REDDIT = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT
                    )


@dataclass
class RedditPost:
    name: str
    title: str
    desc: str
    url: str


def get_reddit_post(subreddit: str, category: str) -> Union[RedditPost, str]:
    if category not in ['hot', 'top', 'new']:
        return 'Invalid Category'
    
    subreddit = REDDIT.subreddit(subreddit)
    
    try:
        subreddit.name # This raises an exception if subreddit is invalid
    except Exception:
        return 'Invalid Subreddit'
    
    post = list(getattr(subreddit, category)(limit=1))[0]
    return RedditPost(name=f'r/{subreddit.display_name}',
                      title=post.title,
                      desc=post.selftext[:200],
                      url=post.url,
                    )