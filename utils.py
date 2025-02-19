import os
import time
import yaml
from dotenv import load_dotenv
from managers.openai_manager import OpenAIManager
from managers.database_manager import DatabaseManager

load_dotenv()

openai = OpenAIManager(api_key=os.getenv("OPENAI_API_KEY"))

with open("prompts.yaml", "r") as f:
    prompt_data = yaml.safe_load(f)


def redaction_enhancent(user_text: str):
    if user_text == "":
        return ""

    database = DatabaseManager()

    # Check if we have a cached response
    cached_response = database.get_cached_response(user_text)
    if cached_response:
        return cached_response

    # If no cached response, proceed with API call
    time.sleep(1)
    model = "gpt-4o-mini"
    res = openai.generate_text(
        system_prompt=prompt_data["redaction_enhancent"]["system_prompt"],
        model=model,
        user_text=user_text,
    )
    if res["status"] == 200:
        database.insert_usage_tokens(
            usage_data={
                "request_id": res["request_id"],
                "total_tokens": res["input_tokens"] + res["output_tokens"],
                "input_tokens": res["input_tokens"],
                "output_tokens": res["output_tokens"],
                "input_str": user_text,
                "output_str": res["content"],
                "model": model,
                "status": res["status"],
            }
        )
        return res["content"]
    else:
        database.insert_usage_tokens(
            usage_data={
                "request_id": res["request_id"],
                "total_tokens": res["input_tokens"] + res["output_tokens"],
                "input_tokens": res["input_tokens"],
                "output_tokens": res["output_tokens"],
                "input_str": user_text,
                "output_str": res["content"],
                "model": model,
            }
        )
        database.insert_error_usage_tokens(
            usage_data={"request_id": res["request_id"], "reason": res["reason"]}
        )
        return res["content"]


def hero_jurney_stories(user_text: str):
    if user_text == "":
        return ""

    # Check if we have a cached response
    database = DatabaseManager()
    cached_response = database.get_cached_response(user_text)
    if cached_response:
        return cached_response

    time.sleep(1)

    model = "gpt-4o-mini"
    res = openai.generate_text(
        system_prompt=prompt_data["hero_jurney"]["system_prompt"],
        model=model,
        user_text=user_text,
    )
    if res["status"] == 200:
        database.insert_usage_tokens(
            usage_data={
                "request_id": res["request_id"],
                "total_tokens": res["input_tokens"] + res["output_tokens"],
                "input_tokens": res["input_tokens"],
                "output_tokens": res["output_tokens"],
                "input_str": user_text,
                "output_str": res["content"],
                "model": model,
                "status": res["status"],
            }
        )
        return res["content"]
    else:
        database.insert_usage_tokens(
            usage_data={
                "request_id": res["request_id"],
                "total_tokens": res["input_tokens"] + res["output_tokens"],
                "input_tokens": res["input_tokens"],
                "output_tokens": res["output_tokens"],
                "input_str": user_text,
                "output_str": res["content"],
                "model": model,
                "status": res["status"],
            }
        )
        database.insert_error_usage_tokens(
            usage_data={"request_id": res["request_id"], "reason": res["reason"]}
        )
        return res["content"]


def narrative_script(user_text: str):
    if user_text == "":
        return ""
    # Check if we have a cached response
    database = DatabaseManager()
    cached_response = database.get_cached_response(user_text)
    if cached_response:
        return cached_response

    time.sleep(1)

    model = "gpt-4o-mini"
    res = openai.generate_text(
        system_prompt=prompt_data["narrative_script"]["system_prompt"],
        model=model,
        user_text=user_text,
    )
    if res["status"] == 200:
        database.insert_usage_tokens(
            usage_data={
                "request_id": res["request_id"],
                "total_tokens": res["input_tokens"] + res["output_tokens"],
                "input_tokens": res["input_tokens"],
                "output_tokens": res["output_tokens"],
                "input_str": user_text,
                "output_str": res["content"],
                "model": model,
                "status": res["status"],
            }
        )

        return res["content"]
    else:
        database.insert_usage_tokens(
            usage_data={
                "request_id": res["request_id"],
                "total_tokens": res["input_tokens"] + res["output_tokens"],
                "input_tokens": res["input_tokens"],
                "output_tokens": res["output_tokens"],
                "input_str": user_text,
                "output_str": res["content"],
                "model": model,
                "status": res["status"],
            }
        )
        database.insert_error_usage_tokens(
            usage_data={"request_id": res["request_id"], "reason": res["reason"]}
        )
        return res["content"]


if __name__ == "__main__":
    response = openai.generate_text(
        system_prompt="You are a helpful assistant.",
        model="gpt-4o-mini",
        user_text="Hello, world!",
    )
    print(response)
