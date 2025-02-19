from sqlalchemy.orm import sessionmaker
from models.database import (
    RedditStories,
    ProcessedStories,
    PromptImagesStories,
    init_db,
    UsageTokens,
    ErrorsUsageTokens,
)
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.engine = init_db()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_reddit_story(self, story_data: dict):
        try:
            story = RedditStories(
                id=story_data["id"],
                created_utc=datetime.fromtimestamp(story_data["created_utc"]),
                title=story_data["title"],
                body=story_data["body"],
                subreddit=story_data["subreddit"],
                author=story_data["author"],
                url=story_data["url"],
                submission_at=story_data["submission_at"],
            )
            self.session.add(story)
            self.session.commit()
            return story
        except Exception as e:
            self.session.rollback()
            raise e

    def insert_processed_story(self, processed_data: dict):
        try:
            processed = ProcessedStories(
                id_stories=processed_data["id_stories"],
                raw_body=processed_data["raw_body"],
                redacted_storie=processed_data["redacted_storie"],
                enhanced_storie=processed_data["enhanced_storie"],
                guion_storie=processed_data["guion_storie"],
            )
            self.session.add(processed)
            self.session.commit()
            return processed
        except Exception as e:
            self.session.rollback()
            raise e

    def insert_prompt_image(self, prompt_data: dict):
        try:
            prompt = PromptImagesStories(
                id_stories=prompt_data["id_stories"],
                image_prompt=prompt_data["image_prompt"],
                init_second=prompt_data["init_second"],
                end_second=prompt_data["end_second"],
                metadata=prompt_data["metadata"],
            )
            self.session.add(prompt)
            self.session.commit()
            return prompt
        except Exception as e:
            self.session.rollback()
            raise e

    def close(self):
        """Close the database session"""
        self.session.close()

    def insert_usage_tokens(self, usage_data: dict):
        try:
            usage = UsageTokens(
                request_id=usage_data["request_id"],
                total_tokens=usage_data["total_tokens"],
                input_tokens=usage_data["input_tokens"],
                output_tokens=usage_data["output_tokens"],
                input_str=usage_data["input_str"],
                output_str=usage_data["output_str"],
                status=usage_data["status"],
            )
            self.session.add(usage)
            self.session.commit()
            return usage
        except Exception as e:
            self.session.rollback()
            raise e

    def insert_error_usage_tokens(self, usage_data: dict):
        try:
            usage = ErrorsUsageTokens(
                request_id=usage_data["request_id"], reason=usage_data["reason"]
            )
            self.session.commit()
            return usage

        except Exception as e:
            self.session.rollback()
            raise e

    def get_cached_response(self, input_text: str) -> str:
        result = (
            self.session.query(UsageTokens.output_str)
            .filter(UsageTokens.input_str == input_text)
            .filter(UsageTokens.status == 200)
            .order_by(UsageTokens.id.desc())
            .first()
        )
        return result[0] if result else None
