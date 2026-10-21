
import os
import re
import uuid

from gtts import gTTS


AUDIO_DIR = os.path.join("output", "story_audio")

LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr"
}


def prepare_story_text(story):
    """Combine the story title, pages, and moral."""

    if not isinstance(story, dict):
        raise ValueError("Invalid story format.")

    pages = story.get("pages", [])

    if not pages:
        raise ValueError("No story pages found.")

    parts = []

    title = story.get("title", "").strip()

    if title:
        parts.append(title)

    for page in pages:
        text = page.get("text", "").strip()

        if text:
            parts.append(text)

    moral = story.get("moral", "").strip()

    if moral:
        parts.append(f"Moral: {moral}")

    full_text = "\n\n".join(parts)

    if not full_text.strip():
        raise ValueError("No text available for narration.")

    return full_text


def generate_story_audio(story, language="English"):
    """Generate an MP3 narration for the selected story."""

    if language not in LANGUAGE_CODES:
        raise ValueError(
            f"Unsupported language: {language}"
        )

    story_text = prepare_story_text(story)

    os.makedirs(AUDIO_DIR, exist_ok=True)

    title = story.get("title", "story")

    safe_title = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        title
    ).strip("_")

    if not safe_title:
        safe_title = "story"

    filename = (
        f"{safe_title[:40]}_{uuid.uuid4().hex[:8]}.mp3"
    )

    audio_path = os.path.join(AUDIO_DIR, filename)

    try:
        tts = gTTS(
            text=story_text,
            lang=LANGUAGE_CODES[language],
            slow=False
        )

        tts.save(audio_path)

    except Exception as error:
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                pass

        raise RuntimeError(
            "Could not generate audio. "
            "Check your internet connection."
        ) from error

    return audio_path
