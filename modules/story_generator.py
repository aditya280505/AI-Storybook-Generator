import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

TEXT_MODEL = os.getenv(
    "GEMINI_TEXT_MODEL",
    "gemini-3.5-flash-lite"
)


def generate_story(
    theme,
    age_group,
    character_name,
    character_age,
    character_description,
    moral,
    number_of_pages,
    language="English"
):
    supported_languages = ["English", "Hindi", "Marathi"]

    if language not in supported_languages:
        raise ValueError(
            f"Unsupported language: {language}. "
            f"Choose from {supported_languages}."
        )

    language_instructions = {
        "English": (
            "Write the title, story text, and moral in English."
        ),
        "Hindi": (
            "Write the title, story text, and moral in natural Hindi "
            "using Devanagari script."
        ),
        "Marathi": (
            "Write the title, story text, and moral in natural Marathi "
            "using Devanagari script."
        )
    }

    prompt = f"""
You are an expert children's storybook author.

Create a completely original, safe, and age-appropriate
children's story.

LANGUAGE INSTRUCTIONS:
Selected Language: {language}
{language_instructions[language]}

The story title, page text, and moral must be in the selected language.
Keep JSON keys and scene descriptions in English.
Scene descriptions must be detailed visual descriptions suitable
for AI image generation.

STORY DETAILS:
Theme: {theme}
Target Age: {age_group}
Main Character: {character_name}
Character Age: {character_age}
Character Appearance: {character_description}
Moral Lesson: {moral}
Number of Pages: {number_of_pages}

REQUIREMENTS:
1. Use simple vocabulary suitable for the target age group.
2. Keep the main character's appearance consistent.
3. Include a clear beginning, middle, and ending.
4. Avoid violence, horror, and inappropriate content.
5. Each page should contain approximately 40-70 words.
6. Each page must have a detailed scene_description in English.
7. Generate exactly {number_of_pages} pages.
8. Return only valid JSON without Markdown code fences.
9. Keep the character's name, age, and appearance consistent
   with the supplied details.
10. Keep all JSON keys in English.
11. Do not translate scene_description into the selected language.

REQUIRED JSON FORMAT:

{{
    "title": "Story title in the selected language",
    "character_profile": {{
        "name": "{character_name}",
        "age": {character_age},
        "appearance": "{character_description}"
    }},
    "moral": "Moral lesson in the selected language",
    "pages": [
        {{
            "page_number": 1,
            "text": "Story text in the selected language",
            "scene_description": "Detailed visual scene description in English"
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    text = response.text.strip()

    # Remove Markdown code fences if Gemini returns them
    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # Parse the JSON response
    try:
        story = json.loads(text)

    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("Gemini returned invalid JSON.")

        try:
            story = json.loads(text[start:end + 1])
        except json.JSONDecodeError as error:
            raise ValueError(
                "Could not parse the story returned by Gemini."
            ) from error

    # Validate the story structure
    if not isinstance(story, dict):
        raise ValueError("Invalid story format.")

    if not isinstance(story.get("pages"), list):
        raise ValueError("Story pages are missing.")

    if len(story["pages"]) != number_of_pages:
        raise ValueError(
            f"Expected {number_of_pages} pages, "
            f"but received {len(story['pages'])}."
        )

    required_fields = ["title", "character_profile", "moral"]

    for field in required_fields:
        if field not in story:
            raise ValueError(f"Missing required story field: {field}")

    for index, page in enumerate(story["pages"], start=1):
        if not isinstance(page, dict):
            raise ValueError(f"Page {index} has an invalid format.")

        for field in ["page_number", "text", "scene_description"]:
            if field not in page:
                raise ValueError(
                    f"Page {index} is missing the field: {field}"
                )

    return story