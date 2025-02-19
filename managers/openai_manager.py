import uuid
from openai import OpenAI


class OpenAIManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, model: str, system_prompt: str, user_text: str):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=0.9,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            print(response)
            return {
                "request_id": response.id,
                "content": response.choices[0].message.content,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "model": model,
                "status": 200,
                "error": "",
            }
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return {
                "request_id": uuid.uuid4(),
                "content": "",
                "input_tokens": 0,
                "output_tokens": 0,
                "model": model,
                "status": 400,
                "error": f"{str(e)}",
            }
