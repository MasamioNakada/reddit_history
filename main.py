import os
import json
import toml
import logging
import pandas as pd
from datetime import datetime
from managers.reddit_manager import RedditManager
from managers.database_manager import DatabaseManager
from models.database import init_db

from utils import redaction_enhancent, hero_jurney_stories, narrative_script

# logging
logging.basicConfig(level=logging.INFO)

# Initialize database if it doesn't exist
if not os.path.exists("reddit_stories.db"):
    logging.info("Database not found. Initializing database...")
    init_db()
    logging.info("Database initialized successfully.")

# Load configuration
config = toml.load("config.toml")
reddit_config = config["reddit"]

# Managers
reddit = RedditManager()
database = DatabaseManager()

# Use configuration settings
subreddits = reddit.reddit.subreddit(reddit_config["subreddit"]).hot(
    limit=reddit_config["story_limit"]
)
logging.info(msg="Subreddits extracted")

data = []
for post in subreddits:
    data.append(
        {
            "id": post.id,
            "created_utc": post.created_utc,
            "title": post.title,
            "body": post.selftext,
            "subreddit": post.subreddit.display_name,
            "author": post.author.name if post.author else None,
            "url": post.url,
            "submission_at": datetime.now(),
        }
    )

df = pd.DataFrame(data)

# Insert base reddit
# Get existing IDs from reddit_stories table
existing_ids = pd.read_sql("SELECT DISTINCT id FROM reddit_stories", database.engine)[
    "id"
].tolist()
# Filter out existing records
df_new = df[~df["id"].isin(existing_ids)]

# Insert only new records
if not df_new.empty:
    df_new.to_sql("reddit_stories", database.engine, if_exists="append", index=False)
    logging.info(msg=f"Inserted {len(df_new)} new records into reddit_stories")
else:
    logging.info(msg="No new records to insert into reddit_stories")
logging.info(msg="Base reddit inserted")

# apply transformation
df["redacted_storie"] = df["body"].apply(redaction_enhancent)
df["enhanced_storie"] = df["redacted_storie"].apply(hero_jurney_stories)
df["guion_storie"] = df["enhanced_storie"].apply(narrative_script)
df["type_storie"] = "hero_jurney"

# rename columns
df.rename(columns={"id": "id_stories", "body": "raw_body"}, inplace=True)
# insert processed_stories
df_processed_stories = df[
    [
        "id_stories",
        "raw_body",
        "redacted_storie",
        "enhanced_storie",
        "guion_storie",
        "type_storie",
    ]
]
# Get existing IDs from processed_stories table
existing_processed_ids = pd.read_sql(
    "SELECT DISTINCT id_stories FROM processed_stories", database.engine
)["id_stories"].tolist()
# Filter out existing records
df_new_processed = df_processed_stories[
    ~df_processed_stories["id_stories"].isin(existing_processed_ids)
]

# Insert only new records
if not df_new_processed.empty:
    df_new_processed.to_sql(
        "processed_stories", database.engine, if_exists="append", index=False
    )
    logging.info(
        msg=f"Inserted {len(df_new_processed)} new records into processed_stories"
    )
else:
    logging.info(msg="No new records to insert into processed_stories")
logging.info(msg="Processed stories inserted")
