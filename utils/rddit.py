import praw
from .secret import CLIENT_ID, CLIENT_SECRET, USER_AGENT


class Reddit:
    def __init__(self, subreddit, category="hot"):
        self.reddit = praw.Reddit(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  user_agent=USER_AGENT)
        self.subreddit = subreddit
        self.category = category.lower()

    def get_post(self):
        try:
            subreddit = self.reddit.subreddit(self.subreddit)
            name = subreddit.name
        except Exception:
            return None

        try:
            post = list(getattr(subreddit, self.category)(limit=1))[0]
        except AttributeError:
            return None

        name = f"r/{subreddit.display_name}"
        title = post.title
        desc = post.selftext
        url = post.url

        if len(desc) > 1001:
            desc = desc[:1001] + '...'
        data = {'name': name, 'title': title, 'desc': desc, 'url': url}
        return data
