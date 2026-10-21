import os
import json
import uuid
from datetime import datetime


LIBRARY_DIR = "output/story_library"
LIBRARY_FILE = os.path.join(LIBRARY_DIR, "stories.json")


def initialize_library():
    """Create the story library directory and JSON file."""
    os.makedirs(LIBRARY_DIR, exist_ok=True)

    if not os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)


def load_story_library():
    """Load all saved stories from the library."""
    initialize_library()

    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as file:
            stories = json.load(file)

        return stories if isinstance(stories, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_story_to_library(story, language="English"):
    """Save a story to the library without overwriting existing stories."""
    if not isinstance(story, dict):
        raise ValueError("Invalid story format.")

    initialize_library()
    stories = load_story_library()

    story_record = {
        "id": str(uuid.uuid4()),
        "title": story.get("title", "Untitled Story"),
        "language": language,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "story": story
    }

    stories.insert(0, story_record)

    with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(stories, file, indent=4, ensure_ascii=False)

    return story_record["id"]


def get_saved_story(story_id):
    """Retrieve one story using its unique ID."""
    stories = load_story_library()

    for record in stories:
        if record.get("id") == story_id:
            return record

    return None


def delete_story_from_library(story_id):
    """Delete a saved story using its unique ID."""
    stories = load_story_library()

    updated_stories = [
        record for record in stories
        if record.get("id") != story_id
    ]

    if len(updated_stories) == len(stories):
        return False

    with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_stories, file, indent=4, ensure_ascii=False)

    return True