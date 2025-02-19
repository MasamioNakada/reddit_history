import os
import praw
from dotenv import load_dotenv

load_dotenv()


class RedditManager:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.user_agent = os.getenv("USER_AGENT")
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )
