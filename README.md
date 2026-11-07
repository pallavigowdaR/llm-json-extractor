# Structured LLM Prompt Pipeline & JSON Extractor

Extracts structured JSON from unstructured text (invoices and resumes) using
an LLM (Google Gemini or OpenAI), parameterized prompt templates with
few-shot examples, and Pydantic validation with automatic retry.

## Features

- Parameterized prompt templates with few-shot examples
- Forced JSON output mode for both Gemini and OpenAI
- Pydantic schema validation
- Auto-retry: validation errors are fed back to the model to self-correct
- Retry with backoff for temporary API errors (503, 429)
- Unit tests using a fake LLM (no API key or cost needed)

## Setup

```bash
git clone https://github.com/<your-username>/llm-json-extractor.git
cd llm-json-extractor
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API key.

## Usage

```bash
python main.py invoice samples/invoice.txt
python main.py resume samples/resume.txt
```

## Example output

```json
{
  "full_name": "Pallavi R",
  "email": "pallavi@example.com",
  "skills": ["Python", "C", "Java", "SQL", "Git", "HTML", "CSS"],
  "education": [
    {
      "institution": "SJC Institute of Technology",
      "degree": "B.E. Computer Science and Engineering",
      "year": "2023 - 2027"
    }
  ]
}
```

## Run tests

```bash
python -m pytest -v
```

## Project structure

```
extractor/
  schemas.py      Pydantic models
  prompts.py      prompt templates + few-shot examples
  llm_client.py   Gemini / OpenAI client with retry
  pipeline.py     prompt -> LLM -> parse -> validate -> retry
tests/            unit tests with a fake LLM
samples/          sample input files
main.py           command-line entry point
```
