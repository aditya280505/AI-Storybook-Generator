import os
import json

from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)

# Use the same model configured for your existing story generator.
TEXT_MODEL = os.getenv(
    "GEMINI_TEXT_MODEL",
    "gemini-3.5-flash-lite"
)


# ============================================================
# HELPER: PARSE JSON RESPONSE
# ============================================================

def parse_json_response(response_text):
    """
    Convert Gemini's JSON response into a Python dictionary.
    """

    if not response_text:
        raise ValueError("Gemini returned an empty response.")

    cleaned_text = response_text.strip()

    # Remove Markdown code fences if present.
    if cleaned_text.startswith("```"):
        lines = cleaned_text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned_text = "\n".join(lines).strip()

        if cleaned_text.lower().startswith("json"):
            cleaned_text = cleaned_text[4:].strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Gemini returned an invalid JSON response."
        ) from error


# ============================================================
# HELPER: VALIDATE STORY
# ============================================================

def validate_story(story):
    """
    Validate the basic structure of a generated story.
    """

    if not isinstance(story, dict):
        raise ValueError("Story must be a dictionary.")

    if not story.get("title"):
        raise ValueError("Story title is missing.")

    pages = story.get("pages")

    if not isinstance(pages, list) or not pages:
        raise ValueError("Story pages are missing.")

    for index, page in enumerate(pages, start=1):

        if not isinstance(page, dict):
            raise ValueError(
                f"Page {index} has an invalid format."
            )

        if not page.get("text"):
            raise ValueError(
                f"Page {index} does not contain story text."
            )

        if not page.get("scene_description"):
            raise ValueError(
                f"Page {index} is missing its scene description."
            )

    return True


# ============================================================
# FEATURE 1A: AI STORY REVIEWER
# ============================================================

def review_story(
    story,
    language="English",
    age_group="Children"
):
    """
    Review a story using Gemini AI.

    Returns:
        Dictionary containing score, feedback and suggestions.
    """

    validate_story(story)

    story_json = json.dumps(
        story,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are an expert children's story editor.

Review the following story carefully.

Story language: {language}
Target audience: {age_group}

STORY:
{story_json}

Evaluate these five criteria:

1. Grammar and language quality
2. Age appropriateness
3. Character consistency
4. Story flow and continuity
5. Moral clarity

Give an overall quality score from 0 to 100.

Be constructive and specific. Do not invent problems that
are not present in the story.

Return ONLY valid JSON using this exact structure:

{{
    "overall_score": 85,
    "grammar": "Feedback about grammar and language",
    "age_appropriateness": "Feedback about suitability",
    "character_consistency": "Feedback about characters",
    "story_flow": "Feedback about story flow",
    "moral_clarity": "Feedback about the moral",
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "suggestions": [
        "Suggestion 1",
        "Suggestion 2"
    ]
}}

The score must be an integer between 0 and 100.
All feedback must be written in {language}.
"""

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )

    result = parse_json_response(response.text)

    # Validate and normalize the score.
    score = result.get("overall_score")

    if not isinstance(score, (int, float)) or isinstance(score, bool):
        raise ValueError("The AI returned an invalid quality score.")

    result["overall_score"] = max(
        0,
        min(100, round(score))
    )

    # Ensure the UI receives lists.
    if not isinstance(result.get("strengths"), list):
        result["strengths"] = []

    if not isinstance(result.get("suggestions"), list):
        result["suggestions"] = []

    return result


# ============================================================
# FEATURE 1B: AUTOMATIC STORY CORRECTION
# ============================================================

def correct_story(
    story,
    review,
    language="English",
    age_group="Children"
):
    """
    Improve a story using the AI review feedback.

    The corrected story retains the original number of pages.
    """

    validate_story(story)

    story_json = json.dumps(
        story,
        ensure_ascii=False,
        indent=2
    )

    review_json = json.dumps(
        review,
        ensure_ascii=False,
        indent=2
    )

    original_page_count = len(story["pages"])

    prompt = f"""
You are an expert children's story editor.

Improve the story using the review feedback below.

LANGUAGE: {language}
TARGET AUDIENCE: {age_group}

ORIGINAL STORY:
{story_json}

AI REVIEW:
{review_json}

INSTRUCTIONS:

1. Correct grammar and awkward wording.
2. Improve clarity, readability and story flow.
3. Resolve character inconsistencies where appropriate.
4. Make the story suitable for the specified age group.
5. Strengthen the moral without changing its core meaning.
6. Preserve the original characters and main storyline.
7. Keep exactly {original_page_count} pages.
8. Write the corrected story in {language}.
9. Preserve the required JSON fields.
10. Every page must contain page_number, text and scene_description.
11. Do not include explanations outside the JSON.

Return ONLY valid JSON with this structure:

{{
    "title": "Corrected story title",
    "character_profile": {{}},
    "moral": "Story moral",
    "pages": [
        {{
            "page_number": 1,
            "text": "Corrected story text",
            "scene_description": "Illustration description"
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )

    corrected_story = parse_json_response(response.text)

    validate_story(corrected_story)

    if len(corrected_story["pages"]) != original_page_count:
        raise ValueError(
            "The corrected story has a different number of pages. "
            "Please try again."
        )

    return corrected_story