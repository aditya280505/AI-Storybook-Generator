import os


def calculate_story_analytics(story, image_paths=None):
    pages = story.get("pages", [])

    page_word_counts = [
        len(page.get("text", "").split())
        for page in pages
    ]

    total_pages = len(pages)
    total_words = sum(page_word_counts)

    average_words_per_page = (
        round(total_words / total_pages, 1)
        if total_pages > 0
        else 0
    )

    reading_time_minutes = (
        max(1, round(total_words / 150))
        if total_words > 0
        else 0
    )

    image_paths = image_paths or []

    successful_images = sum(
        1
        for path in image_paths
        if path and os.path.isfile(path)
    )

    return {
        "story_title": story.get("title", "Untitled Story"),
        "total_pages": total_pages,
        "total_words": total_words,
        "average_words_per_page": average_words_per_page,
        "estimated_reading_time_minutes": reading_time_minutes,
        "successful_images": successful_images,
        "longest_page_words": max(page_word_counts, default=0),
        "shortest_page_words": min(page_word_counts, default=0),
    }