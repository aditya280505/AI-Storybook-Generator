import os
import base64
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

IMAGE_MODEL = os.getenv(
    "GEMINI_IMAGE_MODEL",
    "gemini-2.5-flash-image"
)

# -----------------------------------------
# SAVE IMAGE DATA
# -----------------------------------------

def save_base64_image(
    image_data,
    output_path
):

    with open(
        output_path,
        "wb"
    ) as file:

        file.write(
            base64.b64decode(image_data)
        )


# -----------------------------------------
# GENERATE CHARACTER REFERENCE
# -----------------------------------------

def generate_character_reference(
    character_profile,
    output_path
):

    name = character_profile["name"]
    age = character_profile["age"]
    appearance = character_profile["appearance"]

    prompt = f"""
Create a clean character reference sheet for a
children's storybook.

CHARACTER:

Name: {name}

Age: {age}

Appearance:
{appearance}

Create the character in a friendly children's
picture-book illustration style.

Show the SAME character clearly from multiple
useful views if possible.

Important fixed characteristics:

- Same face
- Same hairstyle
- Same hair color
- Same skin tone
- Same clothing
- Same clothing colors
- Same shoes
- Same accessories
- Same body proportions

Use a simple neutral background.

Do not add written labels or text.

This image will be used as the visual reference
for all subsequent storybook pages.
"""

    response = client.models.generate_images(
        model=IMAGE_MODEL,
        prompt=prompt,
        config={
            "number_of_images": 1,
            "aspect_ratio": "3:4"
        }
    )

    generated = response.generated_images[0]

    image_bytes = generated.image.image_bytes

    with open(
        output_path,
        "wb"
    ) as file:

        file.write(image_bytes)

    return output_path


# -----------------------------------------
# GENERATE PAGE IMAGE
# -----------------------------------------

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
Create a professional children's storybook
illustration.

IMPORTANT:

Use the provided character reference image
as the PRIMARY VISUAL REFERENCE.

The character must remain visually consistent
with the reference.

CHARACTER:

Name: {name}

Age: {age}

Fixed appearance:
{appearance}


CONSISTENCY REQUIREMENTS:

Keep the following unchanged:

- Face
- Eyes
- Nose
- Hairstyle
- Hair color
- Skin tone
- Age
- Clothing
- Clothing colors
- Shoes
- Accessories
- Body proportions

Do not redesign the character.

Do not change the character's clothes.

Do not make the character older or younger.


PAGE:

Page {page_number}


SCENE:

{scene_description}


VISUAL STYLE:

- colorful children's picture book
- warm and friendly
- soft lighting
- polished illustration
- expressive characters
- clean composition
- consistent artistic style
- child-friendly
- high-quality storybook artwork


IMPORTANT:

Do NOT add written story text.

Do NOT add captions.

Do NOT add speech bubbles.

Do NOT add random letters.

The image should contain ONLY the illustration.
"""

    # Read reference image
    with open(
        reference_image_path,
        "rb"
    ) as file:

        reference_bytes = file.read()

    # Use Gemini image model with reference image
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[
            prompt,
            {
                "mime_type": "image/png",
                "data": reference_bytes
            }
        ]
    )

    # Find generated image
    image_saved = False

    if hasattr(response, "candidates"):

        for candidate in response.candidates:

            if not hasattr(candidate, "content"):
                continue

            for part in candidate.content.parts:

                if hasattr(part, "inline_data"):

                    image_data = part.inline_data.data

                    if isinstance(
                        image_data,
                        str
                    ):

                        image_data = base64.b64decode(
                            image_data
                        )

                    with open(
                        output_path,
                        "wb"
                    ) as file:

                        file.write(
                            image_data
                        )

                    image_saved = True
                    break

            if image_saved:
                break

    if not image_saved:

        raise RuntimeError(
            "Gemini did not return an image."
        )

    return output_path