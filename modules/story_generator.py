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
    "gemini-2.5-flash"
)


# -----------------------------------------
# STORY GENERATOR
# -----------------------------------------

def generate_story(
    theme,
    age_group,
    character_name,
    character_age,
    character_description,
    moral,
    number_of_pages
):

    prompt = f"""
You are an expert children's storybook author.

Create a completely original, safe and age-appropriate
children's story.

STORY DETAILS:

Theme:
{theme}

Target Age:
{age_group}

Main Character:
{character_name}

Character Age:
{character_age}

Character Appearance:
{character_description}

Moral Lesson:
{moral}

Number of Pages:
{number_of_pages}


IMPORTANT REQUIREMENTS:

1. The story must be suitable for children.
2. Use simple and engaging vocabulary.
3. Keep the main character visually consistent.
4. The character appearance must NEVER change.
5. Create a clear beginning, middle and ending.
6. Each page must move the story forward.
7. Avoid violence, horror and inappropriate content.
8. Do NOT generate text that should appear inside illustrations.
9. Each page should contain approximately 40-70 words.
10. Give every page a detailed scene description for an illustrator.
11. The scene description must describe only visual elements.
12. Maintain the same art direction throughout the book.


CHARACTER CONSISTENCY:

The following attributes are fixed:

Name:
{character_name}

Age:
{character_age}

Appearance:
{character_description}

These attributes must remain unchanged on every page.


RETURN ONLY VALID JSON.

Required format:

{{
    "title": "Story Title",

    "character_profile": {{
        "name": "{character_name}",
        "age": {character_age},
        "appearance": "{character_description}"
    }},

    "moral": "{moral}",

    "pages": [
        {{
            "page_number": 1,
            "text": "Story text...",
            "scene_description": "Detailed visual scene..."
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        story = json.loads(text)

    except json.JSONDecodeError:

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:

            story = json.loads(
                text[start:end + 1]
            )

        else:

            raise ValueError(
                "Gemini returned invalid JSON."
            )

    return story