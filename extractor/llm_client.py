import os
import time
from dotenv import load_dotenv

load_dotenv()


def _gemini_call(system_prompt: str, user_prompt: str) -> str:
    from google import genai
    from google.genai import types
    from google.genai.errors import ServerError, ClientError

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    temperature=0,
                ),
            )
            return response.text
        except ServerError as e:  # 503 / 500: overloaded, try again
            wait = 2 ** attempt  # 1s, 2s, 4s, 8s, 16s
            print(f"Server busy ({e.code}), retrying in {wait}s...")
            time.sleep(wait)
        except ClientError as e:
            if e.code == 429:  # rate limit: also worth retrying
                wait = 5 * (attempt + 1)
                print(f"Rate limited, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise  # 404, 400, 401 etc. are real mistakes, don't retry

    raise RuntimeError("Gemini is still unavailable after 5 attempts. Try again later.")


def _openai_call(system_prompt: str, user_prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        response_format={"type": "json_object"},  # forces JSON output
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content


def call_llm(system_prompt: str, user_prompt: str) -> str:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        return _gemini_call(system_prompt, user_prompt)
    if provider == "openai":
        return _openai_call(system_prompt, user_prompt)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")