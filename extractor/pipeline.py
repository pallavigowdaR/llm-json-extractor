import json
import re
from pydantic import ValidationError

from .llm_client import call_llm
from .prompts import SYSTEM_PROMPT, build_prompt
from .schemas import SCHEMAS


def _clean_json(raw: str) -> str:
    """Strip ```json fences if the model adds them anyway."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
    return raw


def extract(doc_type: str, text: str, max_retries: int = 2, llm=call_llm) -> dict:
    if doc_type not in SCHEMAS:
        raise ValueError(f"doc_type must be one of {list(SCHEMAS)}")

    schema = SCHEMAS[doc_type]
    prompt = build_prompt(doc_type, text, schema)
    last_error = None

    for attempt in range(max_retries + 1):
        raw = llm(SYSTEM_PROMPT, prompt)
        try:
            data = json.loads(_clean_json(raw))
            return schema.model_validate(data).model_dump()
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
            # feed the error back so the model can self-correct
            prompt += (
                f"\n\nYour previous output was invalid: {e}\n"
                "Return corrected JSON only."
            )

    raise RuntimeError(f"Extraction failed after retries: {last_error}")