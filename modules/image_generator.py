import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL",
    "black-forest-labs/FLUX.1-schnell"
)

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found in .env file."
    )

# IMPORTANT:
# Use automatic provider selection.
# Do NOT force hf-inference.
client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)


def generate_image(prompt, output_path):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    image = client.text_to_image(
        prompt=prompt,
        model=IMAGE_MODEL
    )

    if not isinstance(image, Image.Image):
        raise ValueError(
            "Hugging Face did not return a valid image."
        )

    image = image.convert("RGB")

    image.save(
        output_path,
        format="JPEG",
        quality=95
    )

    return output_path


def generate_character_reference(
    character_profile,
    output_path
):

    name = character_profile["name"]
    age = character_profile["age"]
    appearance = character_profile["appearance"]

    prompt = f"""
Create a professional full-body character reference
for a children's picture storybook.

CHARACTER:

Name: {name}
Age: {age}

FIXED CHARACTER APPEARANCE:

{appearance}

CHARACTER DESIGN:

The character must look friendly, cute,
and appropriate for children.

Keep these visual characteristics fixed:

- same face
- same eyes
- same hairstyle
- same hair color
- same skin tone
- same age
- same clothing
- same clothing colors
- same shoes
- same body proportions

Show the character from head to toe.

ART STYLE:

Colorful children's picture book illustration,
warm friendly atmosphere,
polished digital artwork,
soft lighting,
clean shapes,
expressive face,
high quality,
consistent character design.

BACKGROUND:

Simple clean light background.

IMPORTANT:

This is a character reference sheet.

Do NOT include:

- text
- letters
- captions
- labels
- speech bubbles
- watermark
- logo
"""

    return generate_image(
        prompt,
        output_path
    )


def generate_page_image(
    character_profile,
    scene_description,
    page_number,
    reference_image_path,
    output_path
):

    name = character_profile["name"]
    age = character_profile["age"]
    appearance = character_profile["appearance"]

    prompt = f"""
Create a professional children's picture-book
illustration for Page {page_number}.

MAIN CHARACTER:

Name: {name}
Age: {age}

FIXED CHARACTER APPEARANCE:

{appearance}

CHARACTER CONSISTENCY IS EXTREMELY IMPORTANT.

The character must remain visually consistent
throughout the entire story.

Keep unchanged:

- face
- eyes
- hairstyle
- hair color
- skin tone
- age
- clothing
- clothing colors
- shoes
- accessories
- body proportions

Do NOT redesign the character.

Do NOT change clothing.

Do NOT make the character older or younger.

PAGE SCENE:

{scene_description}

VISUAL STYLE:

Colorful children's picture book illustration,
warm and friendly atmosphere,
polished digital artwork,
soft natural lighting,
expressive character,
clean composition,
consistent art direction,
child-friendly,
high quality.

COMPOSITION:

Create a clear storybook scene.
The main character should be visually prominent.
The environment should support the story action.

IMPORTANT:

The image must contain ONLY the illustration.

Do NOT include:

- story text
- captions
- labels
- speech bubbles
- letters
- random typography
- watermark
- logo
"""

    return generate_image(
        prompt,
        output_path
    )