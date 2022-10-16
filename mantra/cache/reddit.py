import asyncio
import logging
import pickle
import random
from typing import TYPE_CHECKING

import asyncpraw
from aioredis import Redis
from asyncpraw.models import Redditor
from pydantic import BaseModel

from mantra.config import reddit_config
from mantra.core.utils import CommandError

if TYPE_CHECKING:
    from mantra.core.bot import Mantra

logger = logging.getLogger(__name__)


class RedditData(BaseModel):
    url: str
    title: str
    permalink: str
    upvotes: int
    comments: int
    timestamp: int
    author_name: str


class RedditCache:
    def __init__(self, bot: "Mantra") -> None:
        self.bot = bot
        self.subreddits = ["memes"]
        self.reddit = asyncpraw.Reddit(
            client_id=reddit_config.client_id,
            client_secret=reddit_config.client_secret,
            user_agent=reddit_config.user_agent,
        )

    async def get_posts(self) -> None:
        subreddits = [
            await self.reddit.subreddit(subreddit) for subreddit in self.subreddits
        ]

        for subreddit in subreddits:
            await subreddit.load()

            posts = [
                {
                    "url": post.url,
                    "title": post.title,
                    "permalink": post.permalink,
                    "upvotes": post.score,
                    "comments": post.num_comments,
                    "timestamp": post.created_utc,
                    "author_name": post.author.name,
                }
                async for post in subreddit.hot(limit=100)
            ]

            allowed_extensions = (".gif", ".png", ".jpg", ".jpeg")

            posts = list(
                filter(
                    lambda i: any(
                        (i.get("url").endswith(e) for e in allowed_extensions)
                    ),
                    posts,
                )
            )
            obj_list = [RedditData.construct(**post) for post in posts]

            bytes = pickle.dumps(obj_list)
            await self.bot.redis.set(subreddit.display_name, bytes)
            logger.info(f"Posts of {subreddit.display_name} stored in the cache!")

    async def get_data(self, subreddit: str) -> "RedditData":
        data = await self.bot.redis.get(subreddit)
        data = pickle.loads(data)

        if not data:
            raise CommandError("Data hasn't been saved in the cache yet!")
        random.shuffle(data)
        return data

    async def fetch_posts(self) -> None:
        while True:
            await self.get_posts()
            await asyncio.sleep(1800)
