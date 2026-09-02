import os

import streamlit as st

from dotenv import load_dotenv

from modules.story_generator import (
    generate_story
)

from modules.image_generator import (
    generate_character_reference,
    generate_page_image
)

from modules.pdf_generator import (
    create_storybook_pdf
)

from modules.prompt_logger import (
    save_prompt_log,
    load_prompt_logs
)


# =====================================================
# ENVIRONMENT
# =====================================================

load_dotenv()

os.makedirs(
    "assets/images",
    exist_ok=True
)

os.makedirs(
    "output",
    exist_ok=True
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Storybook Generator",
    page_icon="📖",
    layout="wide"
)


# =====================================================
# HEADER
# =====================================================

st.title(
    "📖 AI-Generated Children's Storybook"
)

st.markdown(
    """
### ✨ Create a personalized illustrated
children's storybook using Gemini AI
"""
)

st.divider()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title(
    "🎨 Story Configuration"
)


theme = st.sidebar.selectbox(
    "Story Theme",
    [
        "Adventure",
        "Friendship",
        "Fantasy",
        "Space",
        "Animals",
        "Environment",
        "Magic"
    ]
)


age_group = st.sidebar.selectbox(
    "Target Age Group",
    [
        "4-6 years",
        "6-8 years",
        "8-10 years"
    ]
)


number_of_pages = st.sidebar.slider(
    "Number of Story Pages",
    min_value=4,
    max_value=8,
    value=6
)


st.sidebar.subheader(
    "👦 Main Character"
)


character_name = st.sidebar.text_input(
    "Character Name",
    "Milo"
)


character_age = st.sidebar.number_input(
    "Character Age",
    min_value=4,
    max_value=12,
    value=7
)


character_description = st.sidebar.text_area(
    "Character Appearance",
    """
A 7-year-old boy with curly black hair,
brown eyes, a yellow hoodie, blue shorts,
and red sneakers.
""".strip()
)


moral = st.sidebar.text_input(
    "Moral Lesson",
    "Friendship and kindness make every adventure better."
)


# =====================================================
# CHARACTER PROFILE
# =====================================================

st.header(
    "👤 Character Profile"
)


col1, col2 = st.columns(2)


with col1:

    st.info(
        f"""
**Name:** {character_name}

**Age:** {character_age}

**Appearance:**

{character_description}
"""
    )


with col2:

    st.success(
        f"""
**Theme:** {theme}

**Target Age:** {age_group}

**Pages:** {number_of_pages}

**Moral:** {moral}
"""
    )


# =====================================================
# GENERATE STORY
# =====================================================

if st.button(
    "🧠 Generate Story",
    use_container_width=True
):

    if not os.getenv(
        "GEMINI_API_KEY"
    ):

        st.error(
            "GEMINI_API_KEY not found in .env"
        )

    else:

        try:

            with st.spinner(
                "🧠 Gemini is writing your story..."
            ):

                story = generate_story(
                    theme=theme,
                    age_group=age_group,
                    character_name=character_name,
                    character_age=character_age,
                    character_description=character_description,
                    moral=moral,
                    number_of_pages=number_of_pages
                )

            st.session_state[
                "story"
            ] = story

            st.success(
                "Story generated successfully! 🎉"
            )

        except Exception as e:

            st.error(
                f"Story generation failed:\n{e}"
            )


# =====================================================
# DISPLAY GENERATED STORY
# =====================================================

if "story" in st.session_state:

    story = st.session_state[
        "story"
    ]

    st.divider()

    st.header(
        f"📕 {story['title']}"
    )

    st.write(
        f"**Moral:** {story['moral']}"
    )

    st.divider()

    for page in story["pages"]:

        st.subheader(
            f"📄 Page {page['page_number']}"
        )

        st.write(
            page["text"]
        )

        with st.expander(
            "🔍 Scene Description"
        ):

            st.write(
                page["scene_description"]
            )


# =====================================================
# CHARACTER REFERENCE
# =====================================================

if "story" in st.session_state:

    st.divider()

    st.header(
        "👤 Character Consistency System"
    )

    st.write(
        """
First, the system creates a character reference
image. This reference is then used while generating
the illustrations for each story page.
"""
    )

    if st.button(
        "👤 Generate Character Reference",
        use_container_width=True
    ):

        story = st.session_state[
            "story"
        ]

        reference_path = (
            "assets/images/character_reference.png"
        )

        try:

            with st.spinner(
                "🎨 Creating character reference..."
            ):

                generate_character_reference(
                    character_profile=
                    story["character_profile"],

                    output_path=
                    reference_path
                )

            st.session_state[
                "reference_path"
            ] = reference_path

            st.success(
                "Character reference created! 🎉"
            )

        except Exception as e:

            st.error(
                f"Character reference failed:\n{e}"
            )


# =====================================================
# SHOW CHARACTER REFERENCE
# =====================================================

if (
    "reference_path" in st.session_state
    and
    os.path.exists(
        st.session_state["reference_path"]
    )
):

    st.subheader(
        "🧑 Character Reference"
    )

    st.image(
        st.session_state["reference_path"],
        caption="Fixed Character Reference"
    )


# =====================================================
# GENERATE ILLUSTRATIONS
# =====================================================

if (
    "story" in st.session_state
    and
    "reference_path" in st.session_state
):

    st.divider()

    st.header(
        "🎨 Page Illustrations"
    )

    if st.button(
        "🖼️ Generate All Illustrations",
        use_container_width=True
    ):

        story = st.session_state[
            "story"
        ]

        reference_path = st.session_state[
            "reference_path"
        ]

        total_pages = len(
            story["pages"]
        )

        progress = st.progress(0)

        for index, page in enumerate(
            story["pages"]
        ):

            page_number = page[
                "page_number"
            ]

            image_path = (
                f"assets/images/page_{page_number}.png"
            )

            try:

                with st.spinner(
                    f"🎨 Generating Page {page_number}..."
                ):

                    generate_page_image(
                        character_profile=
                        story["character_profile"],

                        scene_description=
                        page["scene_description"],

                        page_number=
                        page_number,

                        reference_image_path=
                        reference_path,

                        output_path=
                        image_path
                    )

                page[
                    "image_path"
                ] = image_path

                # ---------------------------------
                # PROMPT LOG
                # ---------------------------------

                save_prompt_log(

                    page_number=
                    page_number,

                    prompt=
                    page["scene_description"],

                    issue=
                    "Initial generation may show "
                    "character or visual inconsistencies.",

                    solution=
                    "Used a fixed character profile "
                    "and character reference image "
                    "for generation.",

                    iteration=1
                )

            except Exception as e:

                st.error(
                    f"Page {page_number} failed: {e}"
                )

            progress.progress(
                (index + 1) / total_pages
            )

        st.session_state[
            "story"
        ] = story

        st.success(
            "🎉 All illustrations generated!"
        )


# =====================================================
# PREVIEW
# =====================================================

if "story" in st.session_state:

    story = st.session_state[
        "story"
    ]

    generated_pages = []

    for page in story["pages"]:

        if (
            "image_path" in page
            and
            os.path.exists(
                page["image_path"]
            )
        ):

            generated_pages.append(
                page
            )

    if generated_pages:

        st.divider()

        st.header(
            "📖 Storybook Preview"
        )

        for page in generated_pages:

            col1, col2 = st.columns(
                [1, 1]
            )

            with col1:

                st.image(
                    page["image_path"],
                    caption=
                    f"Illustration - Page {page['page_number']}"
                )

            with col2:

                st.subheader(
                    f"Page {page['page_number']}"
                )

                st.write(
                    page["text"]
                )


# =====================================================
# CREATE PDF
# =====================================================

if "story" in st.session_state:

    story = st.session_state[
        "story"
    ]

    all_images_exist = all(

        "image_path" in page
        and
        os.path.exists(
            page["image_path"]
        )

        for page in story["pages"]
    )

    if all_images_exist:

        st.divider()

        st.header(
            "📕 Final Storybook"
        )

        if st.button(
            "✨ Generate Final PDF",
            use_container_width=True
        ):

            pdf_path = (
                "output/AI_Children_Storybook.pdf"
            )

            try:

                create_storybook_pdf(

                    title=
                    story["title"],

                    pages=
                    story["pages"],

                    output_path=
                    pdf_path,

                    character_name=
                    story[
                        "character_profile"
                    ]["name"],

                    moral=
                    story["moral"]
                )

                st.session_state[
                    "pdf_path"
                ] = pdf_path

                st.success(
                    "🎉 Storybook PDF generated!"
                )

            except Exception as e:

                st.error(
                    f"PDF generation failed:\n{e}"
                )


# =====================================================
# DOWNLOAD PDF
# =====================================================

if (
    "pdf_path" in st.session_state
):

    pdf_path = st.session_state[
        "pdf_path"
    ]

    with open(
        pdf_path,
        "rb"
    ) as file:

        pdf_data = file.read()

    st.download_button(

        label=
        "⬇️ Download Storybook PDF",

        data=
        pdf_data,

        file_name=
        "AI_Children_Storybook.pdf",

        mime=
        "application/pdf",

        use_container_width=True
    )


# =====================================================
# PROMPT LOG
# =====================================================

st.divider()

st.header(
    "📝 Prompt Iteration Log"
)

logs = load_prompt_logs()

if logs:

    for log in logs:

        with st.expander(
            f"Page {log['page']} — "
            f"Iteration {log['iteration']}"
        ):

            st.write(
                "**Prompt / Scene Description:**"
            )

            st.code(
                log["prompt"]
            )

            st.write(
                "**Observed Issue:**"
            )

            st.write(
                log["issue"]
            )

            st.write(
                "**Solution:**"
            )

            st.write(
                log["solution"]
            )

else:

    st.info(
        "Prompt logs will appear after "
        "illustration generation."
    )


# =====================================================
# TECHNICAL ARCHITECTURE
# =====================================================

st.divider()

st.header(
    "⚙️ Technical Architecture"
)

st.code(
"""
                    USER
                      │
                      ▼
             STORY CONFIGURATION
             Theme / Age / Character
                      │
                      ▼
               GEMINI LLM
                      │
                      ▼
              STRUCTURED STORY
                      │
                      ▼
             CHARACTER PROFILE
                      │
                      ▼
         CHARACTER REFERENCE IMAGE
                      │
                      ▼
            PAGE-WISE PROMPTS
                      │
                      ▼
          GEMINI IMAGE GENERATION
                      │
              Reference Image
                    +
              Scene Prompt
                      │
                      ▼
              ILLUSTRATIONS
                      │
                      ▼
              HUMAN REVIEW
                      │
                      ▼
             PDF STORYBOOK
                      │
                      ▼
               PROMPT LOG
""",
language="text"
)


# =====================================================
# PROJECT INFORMATION
# =====================================================

st.divider()

st.header(
    "ℹ️ Project Information"
)

st.markdown(
"""
### AI Components

**1. Gemini LLM**
- Story generation
- Character profile creation
- Page-wise scene descriptions

**2. Gemini Image Generation**
- Character reference
- Page illustrations

### Supporting Technologies

- Python
- Streamlit
- Pillow
- ReportLab
- JSON
- Prompt Engineering

### Human-in-the-Loop

The human reviews generated content,
checks character consistency and selects
the final storybook output.
"""
)