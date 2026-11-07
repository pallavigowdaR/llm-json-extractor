import json
import pytest

from extractor.pipeline import extract

VALID_INVOICE = {
    "invoice_number": "INV-1",
    "invoice_date": "2025-09-12",
    "vendor_name": "Shop",
    "line_items": [
        {"description": "Pen", "quantity": 2, "unit_price": 10, "total": 20}
    ],
    "total_amount": 20,
}

VALID_RESUME = {
    "full_name": "Anita S.",
    "email": "anita@mail.com",
    "skills": ["Python", "SQL"],
    "education": [{"institution": "XYZ College", "degree": "B.E. CSE", "year": "2024"}],
}


def test_valid_json_passes():
    fake = lambda s, u: json.dumps(VALID_INVOICE)
    result = extract("invoice", "some text", llm=fake)
    assert result["invoice_number"] == "INV-1"
    assert result["currency"] == "INR"  # default applied


def test_valid_resume_passes():
    fake = lambda s, u: json.dumps(VALID_RESUME)
    result = extract("resume", "some text", llm=fake)
    assert result["full_name"] == "Anita S."
    assert "Python" in result["skills"]


def test_markdown_fences_are_stripped():
    fake = lambda s, u: "```json\n" + json.dumps(VALID_INVOICE) + "\n```"
    assert extract("invoice", "x", llm=fake)["total_amount"] == 20


def test_retry_recovers_from_bad_output():
    calls = {"n": 0}

    def flaky(s, u):
        calls["n"] += 1
        return "not json at all" if calls["n"] == 1 else json.dumps(VALID_INVOICE)

    assert extract("invoice", "x", llm=flaky)["invoice_number"] == "INV-1"
    assert calls["n"] == 2


def test_fails_after_max_retries():
    with pytest.raises(RuntimeError):
        extract("invoice", "x", max_retries=1, llm=lambda s, u: "garbage")


def test_missing_required_field_fails():
    bad = {"invoice_number": "INV-1"}  # missing most fields
    with pytest.raises(RuntimeError):
        extract("invoice", "x", max_retries=0, llm=lambda s, u: json.dumps(bad))


def test_empty_name_is_rejected():
    bad = dict(VALID_RESUME, full_name="")
    with pytest.raises(RuntimeError):
        extract("resume", "x", max_retries=0, llm=lambda s, u: json.dumps(bad))


def test_invalid_doc_type():
    with pytest.raises(ValueError):
        extract("passport", "x")