import os
import streamlit as st
from dotenv import load_dotenv

from modules.story_generator import generate_story

from modules.image_generator import (
    generate_character_reference,
    generate_page_image
)

from modules.pdf_generator import create_storybook_pdf

from modules.prompt_logger import (
    save_prompt_log,
    load_prompt_logs
)

from modules.story_analytics import calculate_story_analytics

from modules.story_library import (
    initialize_library,
    load_story_library,
    save_story_to_library,
    get_saved_story,
    delete_story_from_library
)

from modules.story_reviewer import review_story, correct_story

from modules.voice_narrator import generate_story_audio



# ============================================================
# 1. INITIALIZATION
# ============================================================

load_dotenv()

os.makedirs("assets/images", exist_ok=True)
os.makedirs("output", exist_ok=True)

initialize_library()

st.set_page_config(
    page_title="AI Storybook Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Children's Storybook Generator")

st.markdown(
    """
    Create personalized children's stories with AI-generated
    illustrations, multilingual support, analytics, and PDF export.
    """
)


# ============================================================
# 2. SESSION STATE
# ============================================================

if "story" not in st.session_state:
    st.session_state["story"] = None

if "story_language" not in st.session_state:
    st.session_state["story_language"] = "English"

if "loaded_story_id" not in st.session_state:
    st.session_state["loaded_story_id"] = None

if "confirm_delete_story" not in st.session_state:
    st.session_state["confirm_delete_story"] = None


# ============================================================
# 3. SIDEBAR: STORY CONFIGURATION
# ============================================================

st.sidebar.header("⚙️ Story Configuration")

theme = st.sidebar.selectbox(
    "🎨 Select Story Theme",
    [
        "Adventure",
        "Fantasy",
        "Friendship",
        "Animals",
        "Space",
        "Nature",
        "Magic",
        "Science",
        "Kindness"
    ]
)

age_group = st.sidebar.selectbox(
    "👶 Target Age Group",
    [
        "3-5 years",
        "6-8 years",
        "9-12 years"
    ]
)

# FEATURE 5: MULTILINGUAL STORY GENERATION

language = st.sidebar.selectbox(
    "🌐 Story Language",
    [
        "English",
        "Hindi",
        "Marathi"
    ],
    key="language_selector"
)

number_of_pages = st.sidebar.slider(
    "📄 Number of Pages",
    min_value=4,
    max_value=8,
    value=4
)

character_name = st.sidebar.text_input(
    "🧒 Character Name",
    value="Milo"
)

character_age = st.sidebar.number_input(
    "🎂 Character Age",
    min_value=1,
    max_value=15,
    value=7
)

character_description = st.sidebar.text_area(
    "👕 Character Appearance",
    value=(
        "A cheerful young child with short brown hair, "
        "bright eyes, a blue shirt, and brown shorts."
    )
)

moral = st.sidebar.text_input(
    "💡 Moral Lesson",
    value="Kindness and helping others"
)


# ============================================================
# 4. GENERATE STORY
# ============================================================

st.header("✨ Create Your Story")

if st.button(
    "🚀 Generate Story",
    type="primary",
    use_container_width=True
):

    if not os.getenv("GEMINI_API_KEY"):
        st.error(
            "GEMINI_API_KEY is missing. Please check your .env file."
        )

    elif not character_name.strip():
        st.error("Please enter a character name.")

    elif not character_description.strip():
        st.error("Please describe the character's appearance.")

    elif not moral.strip():
        st.error("Please enter a moral lesson.")

    else:
        try:
            with st.spinner(
                f"Generating your story in {language}..."
            ):

                story = generate_story(
                    theme=theme,
                    age_group=age_group,
                    character_name=character_name.strip(),
                    character_age=int(character_age),
                    character_description=character_description.strip(),
                    moral=moral.strip(),
                    number_of_pages=number_of_pages,
                    language=language
                )

            # Remove old illustration paths from the new story.
            for page in story.get("pages", []):
                page.pop("image_path", None)

            st.session_state["story"] = story
            st.session_state["story_language"] = language
            st.session_state["loaded_story_id"] = None

            st.success("Your story has been generated!")

        except Exception as error:
            st.error(f"Story generation failed: {error}")


# ============================================================
# 5. DISPLAY CURRENT STORY
# ============================================================

story = st.session_state.get("story")

if story:

    st.divider()

    st.header("📖 Your Story")

    st.subheader(story.get("title", "Untitled Story"))

    st.caption(
        f"Language: {st.session_state.get('story_language', 'English')}"
    )

    character_profile = story.get("character_profile", {})

    with st.expander("🧒 Character Profile", expanded=False):

        st.write(
            "**Name:**",
            character_profile.get("name", "Not specified")
        )

        st.write(
            "**Age:**",
            character_profile.get("age", "Not specified")
        )

        st.write(
            "**Appearance:**",
            character_profile.get("appearance", "Not specified")
        )

    for page in story.get("pages", []):

        page_number = page.get("page_number", "?")

        with st.container(border=True):

            st.markdown(f"### 📄 Page {page_number}")

            st.write(page.get("text", ""))

            with st.expander("🎨 Scene Description"):

                st.write(
                    page.get(
                        "scene_description",
                        "No scene description available."
                    )
                )

            image_path = page.get("image_path")

            if image_path and os.path.isfile(image_path):

                st.image(
                    image_path,
                    caption=f"Illustration for Page {page_number}",
                    use_container_width=True
                )

    st.info(
        f"**Moral:** {story.get('moral', 'Not specified')}"
    )


    # ========================================================
    # 6. FEATURE 4: SAVE STORY TO LIBRARY
    # ========================================================

    st.divider()

    st.subheader("💾 Save Your Story")

    if st.button(
        "Save Story to Library",
        key="save_current_story",
        use_container_width=True
    ):

        try:
            story_id = save_story_to_library(
                story,
                language=st.session_state.get(
                    "story_language",
                    "English"
                )
            )

            st.session_state["loaded_story_id"] = story_id

            st.success(
                "Story saved successfully to your Story Library!"
            )

        except Exception as error:
            st.error(f"Could not save story: {error}")


    # ========================================================
    # 7. FEATURE 7: STORY ANALYTICS
    # ========================================================

    st.divider()

    st.header("📊 Story Analytics")

    try:

        image_paths = [
            page.get("image_path")
            for page in story.get("pages", [])
        ]

        analytics = calculate_story_analytics(
            story,
            image_paths=image_paths
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Pages",
                analytics["total_pages"]
            )

        with col2:
            st.metric(
                "Total Words",
                analytics["total_words"]
            )

        with col3:
            st.metric(
                "Avg. Words per Page",
                analytics["average_words_per_page"]
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric(
                "Reading Time",
                f"{analytics['estimated_reading_time_minutes']} min"
            )

        with col5:
            st.metric(
                "Generated Images",
                analytics["successful_images"]
            )

        with col6:
            st.metric(
                "Longest Page",
                f"{analytics['longest_page_words']} words"
            )

        with st.expander("View Detailed Analytics"):

            st.write(
                "**Story Title:**",
                analytics["story_title"]
            )

            st.write(
                "**Shortest Page:**",
                f"{analytics['shortest_page_words']} words"
            )

            st.write(
                "**Selected Language:**",
                st.session_state.get(
                    "story_language",
                    "English"
                )
            )

    except Exception as error:
        st.warning(f"Analytics could not be calculated: {error}")


    # ========================================================
    # 8. GENERATE CHARACTER REFERENCE
    # ========================================================

    st.divider()

    st.header("🧑 Character Reference Image")

    character_reference_path = "assets/images/character_reference.jpg"

    if st.button(
        "🎨 Generate Character Reference",
        key="generate_character_reference"
    ):

        try:
            with st.spinner("Generating character reference..."):

                generate_character_reference(
                    character_profile,
                    character_reference_path
                )

            if os.path.isfile(character_reference_path):
                st.success("Character reference generated!")

                st.image(
                    character_reference_path,
                    caption="Main Character Reference",
                    use_container_width=True
                )

            else:
                st.warning(
                    "The function finished, but no image file was found."
                )

        except Exception as error:
            st.error(
                f"Character reference generation failed: {error}"
            )

    elif os.path.isfile(character_reference_path):

        st.image(
            character_reference_path,
            caption="Saved Character Reference",
            use_container_width=True
        )


    # ========================================================
    # 9. GENERATE PAGE ILLUSTRATIONS
    # ========================================================

    st.divider()

    st.header("🖼️ Generate Story Illustrations")

    if st.button(
        "Generate All Page Illustrations",
        key="generate_page_illustrations",
        use_container_width=True
    ):

        if not os.path.isfile(character_reference_path):

            st.warning(
                "Generate the character reference image first."
            )

        else:

            progress = st.progress(0)

            try:

                total_pages = len(story.get("pages", []))

                for index, page in enumerate(
                    story.get("pages", []),
                    start=1
                ):

                    page_number = page["page_number"]

                    output_path = (
                        f"assets/images/page_{page_number}.jpg"
                    )

                    with st.spinner(
                        f"Generating illustration {index}/{total_pages}..."
                    ):

                        generate_page_image(
                            character_profile,
                            page["scene_description"],
                            page_number,
                            character_reference_path,
                            output_path
                        )

                    if os.path.isfile(output_path):

                        page["image_path"] = output_path

                    else:

                        page.pop("image_path", None)

                    progress.progress(index / total_pages)

                st.session_state["story"] = story

                st.success("Illustration generation completed!")

                st.rerun()

            except Exception as error:

                st.error(
                    f"Illustration generation failed: {error}"
                )


    # ========================================================
    # 10. DOWNLOAD STORYBOOK PDF
    # ========================================================

    st.divider()

    st.header("📕 Export Storybook")

    if st.button(
        "Generate Storybook PDF",
        key="generate_storybook_pdf",
        use_container_width=True
    ):

        pdf_path = "output/AI_Children_Storybook.pdf"

        try:

            with st.spinner("Creating your storybook PDF..."):

                create_storybook_pdf(
                    story.get("title", "AI Children's Storybook"),
                    story.get("pages", []),
                    pdf_path,
                    character_profile.get("name", "Character"),
                    story.get("moral", "")
                )

            if os.path.isfile(pdf_path):

                st.success("Your storybook PDF is ready!")

                with open(pdf_path, "rb") as pdf_file:

                    st.download_button(
                        label="⬇️ Download Storybook PDF",
                        data=pdf_file.read(),
                        file_name="AI_Children_Storybook.pdf",
                        mime="application/pdf",
                        key="download_storybook_pdf"
                    )

            else:

                st.error("PDF file was not created.")

        except Exception as error:

            st.error(f"PDF generation failed: {error}")



# ==========================================
# AI VOICE NARRATION
# ==========================================

st.divider()
st.header("🔊 AI Voice Narration")

current_story = st.session_state.get("story")

if current_story:

    narration_language = st.session_state.get(
        "language",
        "English"
    )

    st.write(
        f"Generate audio narration in {narration_language}."
    )

    if st.button(
        "🎙️ Generate Audio",
        key="generate_story_audio_button"
    ):
        try:
            with st.spinner("Generating story audio..."):

                audio_path = generate_story_audio(
                    current_story,
                    language=narration_language
                )

                st.session_state["story_audio_path"] = audio_path
                st.session_state["story_audio_title"] = (
                    current_story.get("title", "")
                )
                st.session_state["story_audio_language"] = (
                    narration_language
                )

            st.success("Audio generated successfully!")

        except Exception as error:
            st.error(f"Audio generation failed: {error}")

    audio_path = st.session_state.get("story_audio_path")

    audio_matches_story = (
        st.session_state.get("story_audio_title")
        == current_story.get("title", "")
        and st.session_state.get("story_audio_language")
        == narration_language
    )

    if audio_path and audio_matches_story:

        if os.path.isfile(audio_path):

            st.subheader("🎧 Listen to Your Story")

            st.audio(
                audio_path,
                format="audio/mp3"
            )

            with open(audio_path, "rb") as audio_file:
                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio_file.read(),
                    file_name=os.path.basename(audio_path),
                    mime="audio/mpeg",
                    key="download_story_audio_button"
                )

        else:
            st.warning("Audio file not found. Generate it again.")

else:
    st.info("Please generate a story first.")


# ============================================================
# FEATURE 1: AI STORY REVIEWER & AUTOMATIC CORRECTION
# ============================================================

st.divider()
st.header("🤖 AI Story Reviewer & Automatic Correction")

current_story = st.session_state.get("story")

if current_story:

    review_language = st.session_state.get(
        "language", "English"
    )

    review_age_group = st.session_state.get(
        "age_group", "Children"
    )

    # --------------------------------------------------------
    # REVIEW STORY
    # --------------------------------------------------------

    if st.button(
        "🔍 Review My Story",
        key="review_story_button"
    ):

        try:
            with st.spinner(
                "AI is reviewing your story..."
            ):

                review_result = review_story(
                    current_story,
                    language=review_language,
                    age_group=review_age_group
                )

                st.session_state["story_review"] = review_result

                # Remove outdated correction results.
                st.session_state.pop(
                    "corrected_story",
                    None
                )

            st.success("Story review completed!")

        except Exception as error:
            st.error(f"Story review failed: {error}")

    # --------------------------------------------------------
    # DISPLAY REVIEW RESULTS
    # --------------------------------------------------------

    review_result = st.session_state.get(
        "story_review"
    )

    if review_result:

        st.subheader("📊 Story Review Results")

        score = review_result.get(
            "overall_score", 0
        )

        st.metric(
            "Story Quality Score",
            f"{score}/100"
        )

        st.progress(score / 100)

        st.markdown("### 📝 Review Details")

        st.write("**Grammar & Language:**")
        st.write(
            review_result.get(
                "grammar", "No feedback available."
            )
        )

        st.write("**Age Appropriateness:**")
        st.write(
            review_result.get(
                "age_appropriateness",
                "No feedback available."
            )
        )

        st.write("**Character Consistency:**")
        st.write(
            review_result.get(
                "character_consistency",
                "No feedback available."
            )
        )

        st.write("**Story Flow:**")
        st.write(
            review_result.get(
                "story_flow", "No feedback available."
            )
        )

        st.write("**Moral Clarity:**")
        st.write(
            review_result.get(
                "moral_clarity", "No feedback available."
            )
        )

        with st.expander("✅ Story Strengths"):

            strengths = review_result.get(
                "strengths", []
            )

            if strengths:
                for item in strengths:
                    st.write(f"• {item}")
            else:
                st.write("No strengths were returned.")

        with st.expander("💡 Improvement Suggestions"):

            suggestions = review_result.get(
                "suggestions", []
            )

            if suggestions:
                for item in suggestions:
                    st.write(f"• {item}")
            else:
                st.write("No suggestions were returned.")

        # ----------------------------------------------------
        # AUTOMATIC CORRECTION
        # ----------------------------------------------------

        st.markdown("### ✨ Improve Your Story")

        if st.button(
            "✨ Apply AI Corrections",
            key="correct_story_button"
        ):

            try:
                with st.spinner(
                    "AI is improving your story..."
                ):

                    corrected = correct_story(
                        current_story,
                        review_result,
                        language=review_language,
                        age_group=review_age_group
                    )

                    st.session_state[
                        "corrected_story"
                    ] = corrected

                st.success(
                    "Corrected story generated successfully!"
                )

            except Exception as error:
                st.error(
                    f"Story correction failed: {error}"
                )

    # --------------------------------------------------------
    # DISPLAY CORRECTED STORY
    # --------------------------------------------------------

    corrected_story = st.session_state.get(
        "corrected_story"
    )

    if corrected_story:

        st.divider()
        st.subheader("✨ Corrected Story")

        st.markdown(
            f"### {corrected_story.get('title', 'Untitled Story')}"
        )

        for page in corrected_story.get("pages", []):

            page_number = page.get(
                "page_number", ""
            )

            st.markdown(
                f"**Page {page_number}**"
            )

            st.write(page.get("text", ""))

            scene = page.get("scene_description")

            if scene:
                with st.expander("🎨 Scene Description"):
                    st.write(scene)

        st.markdown("**Moral:**")

        st.write(
            corrected_story.get("moral", "")
        )

        # ----------------------------------------------------
        # SAVE CORRECTED STORY
        # ----------------------------------------------------

        if st.button(
            "💾 Save Corrected Story to Library",
            key="save_corrected_story_button"
        ):

            try:
                from modules.story_library import (
                    save_story_to_library
                )

                save_story_to_library(
                    corrected_story,
                    language=review_language
                )

                st.success(
                    "Corrected story saved to Story Library!"
                )

            except Exception as error:
                st.error(
                    f"Could not save corrected story: {error}"
                )

else:

    st.info(
        "📖 Generate a story first to use the AI Story Reviewer."
    )

# ============================================================
# 11. FEATURE 4: STORY HISTORY & LIBRARY
# ============================================================

st.divider()

st.header("📚 Story History & Library")

st.write(
    "View, reopen, and delete previously saved stories."
)

try:

    saved_stories = load_story_library()

    if not saved_stories:

        st.info(
            "Your Story Library is empty. Generate a story "
            "and click 'Save Story to Library'."
        )

    else:

        st.metric(
            "Total Saved Stories",
            len(saved_stories)
        )

        for record in saved_stories:

            story_id = record.get("id")
            title = record.get("title", "Untitled Story")
            saved_language = record.get("language", "English")
            saved_at = record.get("saved_at", "Unknown date")

            with st.expander(f"📖 {title}"):

                st.caption(
                    f"Language: {saved_language} | Saved: {saved_at}"
                )

                col1, col2 = st.columns(2)

                # OPEN A SAVED STORY
                with col1:

                    if st.button(
                        "📖 Open Story",
                        key=f"open_{story_id}"
                    ):

                        selected_record = get_saved_story(story_id)

                        if selected_record:

                            st.session_state["story"] = (
                                selected_record.get("story")
                            )

                            st.session_state["story_language"] = (
                                selected_record.get(
                                    "language",
                                    "English"
                                )
                            )

                            st.session_state["loaded_story_id"] = (
                                story_id
                            )

                            st.rerun()

                        else:

                            st.error("Saved story could not be found.")

                # REQUEST STORY DELETION
                with col2:

                    if st.button(
                        "🗑️ Delete Story",
                        key=f"delete_{story_id}"
                    ):

                        st.session_state["confirm_delete_story"] = (
                            story_id
                        )

                # CONFIRM DELETION
                if (
                    st.session_state.get("confirm_delete_story")
                    == story_id
                ):

                    st.warning(
                        f"Are you sure you want to delete '{title}'?"
                    )

                    confirm_col1, confirm_col2 = st.columns(2)

                    with confirm_col1:

                        if st.button(
                            "Yes, Delete",
                            key=f"confirm_delete_{story_id}"
                        ):

                            try:

                                deleted = delete_story_from_library(
                                    story_id
                                )

                                st.session_state.pop(
                                    "confirm_delete_story",
                                    None
                                )

                                if deleted:

                                    st.success("Story deleted.")
                                    st.rerun()

                                else:

                                    st.error(
                                        "Story could not be found."
                                    )

                            except Exception as error:

                                st.error(
                                    f"Could not delete story: {error}"
                                )

                    with confirm_col2:

                        if st.button(
                            "Cancel",
                            key=f"cancel_delete_{story_id}"
                        ):

                            st.session_state.pop(
                                "confirm_delete_story",
                                None
                            )

                            st.rerun()

except Exception as error:

    st.error(f"Could not load the Story Library: {error}")


# ============================================================
# 12. PROMPT LOGS
# ============================================================

st.divider()

with st.expander("📝 Prompt Logs"):

    try:

        logs = load_prompt_logs()

        if logs:

            st.write("Previous prompt iterations:")

            st.json(logs)

        else:

            st.info("No prompt logs available yet.")

    except Exception as error:

        st.warning(f"Could not load prompt logs: {error}")


# ============================================================
# 13. TECHNICAL ARCHITECTURE
# ============================================================

with st.expander("🛠️ Technical Architecture"):

    st.markdown(
        """
        **Frontend**
        - Streamlit

        **Story Generation**
        - Google Gemini API
        - Structured JSON story output
        - English, Hindi, and Marathi support

        **Image Generation**
        - Hugging Face Inference Providers
        - FLUX image generation model

        **PDF Generation**
        - ReportLab

        **Story Library**
        - JSON-based persistent storage

        **Analytics**
        - Word count
        - Page count
        - Average words per page
        - Estimated reading time
        - Generated image count

        **Logging**
        - Prompt iteration history
        """
    )


# ============================================================
# 14. PROJECT INFORMATION
# ============================================================

with st.expander("ℹ️ About This Project"):

    st.markdown(
        """
        The AI Children's Storybook Generator creates personalized
        children's stories using generative AI.

        Users can select a theme, age group, character, language,
        page count, and moral lesson.

        The application supports story analytics, illustration
        generation, PDF export, and a persistent Story Library.
        """
    )