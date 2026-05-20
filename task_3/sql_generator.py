import os
from google import genai

from prompts.templates import (
    SCHEMA_CONTEXT,
    DECOMPOSITION_PROMPT,
    GENERATION_PROMPT,
    FIX_PROMPT
)


def get_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def clean_output(text):

    if not text:
        return ""

    return (
        text
        .replace("```json", "")
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )


def decompose_question(question):

    client = get_client()

    prompt = DECOMPOSITION_PROMPT.format(
        question=question,
        schema=SCHEMA_CONTEXT
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )

    return clean_output(response.text)


def generate_sql(decomposition_json):

    client = get_client()

    prompt = GENERATION_PROMPT.format(
        decomposition_json=decomposition_json,
        schema=SCHEMA_CONTEXT
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )

    return clean_output(response.text)


def fix_sql(question, bad_sql, error_msg):

    client = get_client()

    prompt = FIX_PROMPT.format(
        question=question,
        bad_sql=bad_sql,
        error_msg=error_msg
    )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )

    return clean_output(response.text)