import json
from pydantic import BaseModel

SYSTEM_PROMPT = (
    "You are a precise data-extraction engine. "
    "Return ONLY valid JSON matching the given schema. "
    "No markdown, no explanations. Use null for missing optional fields. "
    "Never invent information that is not in the text."
)

FEW_SHOT = {
    "invoice": {
        "input": "INV-204 dated 5 Mar 2025. From Acme Traders to Ravi Kumar. "
                 "2 x Keyboard @ 500 = 1000. Tax 180. Total Rs 1180.",
        "output": {
            "invoice_number": "INV-204",
            "invoice_date": "2025-03-05",
            "vendor_name": "Acme Traders",
            "customer_name": "Ravi Kumar",
            "line_items": [
                {"description": "Keyboard", "quantity": 2,
                 "unit_price": 500, "total": 1000}
            ],
            "subtotal": 1000,
            "tax": 180,
            "total_amount": 1180,
            "currency": "INR",
        },
    },
    "resume": {
        "input": "Anita S. anita@mail.com. B.E. CSE, XYZ College, 2024. "
                 "Skills: Python, SQL. Built a chatbot during 3-month internship.",
        "output": {
            "full_name": "Anita S.",
            "email": "anita@mail.com",
            "phone": None,
            "skills": ["Python", "SQL"],
            "education": [
                {"institution": "XYZ College", "degree": "B.E. CSE", "year": "2024"}
            ],
            "experience_summary": "Built a chatbot during a 3-month internship.",
            "total_experience_years": 0.25,
        },
    },
}

USER_TEMPLATE = """Task: Extract a {doc_type} from the text below.

JSON schema:
{schema}

Example input:
{ex_in}

Example output:
{ex_out}

Now extract from this text:
\"\"\"
{text}
\"\"\"
"""


def build_prompt(doc_type: str, text: str, schema: type[BaseModel]) -> str:
    shot = FEW_SHOT[doc_type]
    return USER_TEMPLATE.format(
        doc_type=doc_type,
        schema=json.dumps(schema.model_json_schema(), indent=2),
        ex_in=shot["input"],
        ex_out=json.dumps(shot["output"], indent=2),
        text=text,
    )