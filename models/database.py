from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class RedditStories(Base):
    __tablename__ = "reddit_stories"

    id = Column(String, primary_key=True, unique=True)
    created_utc = Column(DateTime, nullable=False)
    title = Column(String)
    body = Column(String)
    subreddit = Column(String)
    author = Column(String)
    url = Column(String)
    submission_at = Column(DateTime, nullable=False, default=datetime.now())

    # Relationships
    # processed_stories = relationship('ProcessedStories', back_populates='reddit_story')
    # prompt_images = relationship('PromptImagesStories', back_populates='reddit_story')


class ProcessedStories(Base):
    __tablename__ = "processed_stories"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_stories = Column(String, nullable=False)
    raw_body = Column(String)
    redacted_storie = Column(String)
    enhanced_storie = Column(String)
    guion_storie = Column(String)
    type_storie = Column(String)

    # Relationship
    # reddit_story = relationship('RedditStories', back_populates='processed_stories')


class PromptImagesStories(Base):
    __tablename__ = "prompt_images_stories"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_stories = Column(String, nullable=False)
    image_prompt = Column(String)
    init_second = Column(Integer)
    end_second = Column(Integer)
    metadata_stories = Column(JSON)

    # Relationship
    # reddit_story = relationship('RedditStories', back_populates='prompt_images')


class UsageTokens(Base):
    __tablename__ = "usage_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now())
    total_tokens = Column(Integer)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    input_str = Column(String)
    output_str = Column(String)
    status = Column(Integer)


class ErrorsUsageTokens(Base):
    __tablename__ = "errors_usage_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, nullable=False)
    reason = Column(String)
    date = Column(DateTime, nullable=False, default=datetime.now())


def init_db():
    engine = create_engine("sqlite:///reddit_stories.db")
    Base.metadata.create_all(engine)
    return engine


if __name__ == "__main__":
    init_db()
