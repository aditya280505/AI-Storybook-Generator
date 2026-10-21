# 📚 AI-Generated Children's Storybook

> An AI-powered web application that creates illustrated children's storybooks based on user-provided themes, characters, age groups, and moral lessons.

### 🚀 Live Demo

**[▶️ Try the AI Storybook Generator](https://ai-storybook-generator-jfs5ycyxu6dkga23dtyyfw.streamlit.app/)**

---

## 📌 Project Overview

The application uses **Google Gemini** for story generation, **Hugging Face Inference Providers** for AI-generated illustrations, and **ReportLab** to assemble the final storybook into a PDF.

## 🚀 Features

* ✨ AI-generated children's stories
* 🎨 AI-generated page illustrations
* 👦 Character description consistency across pages
* 🧒 Age-appropriate story generation
* 📖 Multi-page storybook creation
* 💡 Moral-based storytelling
* 📝 Page-wise scene descriptions
* 🔄 Prompt iteration and logging
* 👀 Human editorial review
* 📝 AI Story Reviewer with story improvement and correction capabilities
* 🔊 AI Voice Narration with English, Hindi, and Marathi support
* 📄 Automatic PDF storybook generation
* 📚 Story Library for managing generated stories
* 📊 Story analytics
* 🌐 Interactive Streamlit web interface

## 🏗️ Project Architecture

```text
User
  ↓
Story Configuration
  ↓
Google Gemini
  ↓
Structured Story + Character Profile
  ↓
Page-wise Scene Descriptions
  ↓
Hugging Face Inference Providers
  ↓
AI-Generated Illustrations
  ↓
AI Story Reviewer & Human Review
  ↓
AI Voice Narration
  ↓
Story Library & Analytics
  ↓
ReportLab PDF Generator
  ↓
📖 Final Illustrated Storybook
```

## 🛠️ Technologies Used

| Technology                       | Purpose                                 |
| -------------------------------- | --------------------------------------- |
| Python                           | Core programming language               |
| Streamlit                        | Interactive web application             |
| Google Gemini API                | Story generation and AI-powered content |
| Hugging Face Inference Providers | AI image generation                     |
| FLUX.1-schnell                   | Storybook illustration generation       |
| gTTS                             | Text-to-speech narration                |
| Pillow                           | Image processing                        |
| ReportLab                        | PDF generation                          |
| Pandas                           | Data processing and analytics           |
| JSON                             | Structured story and prompt data        |
| python-dotenv                    | Environment variable management         |
| Git & GitHub                     | Version control and repository hosting  |

## 📂 Project Structure

```text
AI_STORYBOOK/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── modules/
│   ├── __init__.py
│   ├── story_generator.py
│   ├── image_generator.py
│   ├── pdf_generator.py
│   ├── prompt_logger.py
│   ├── story_analytics.py
│   ├── story_library.py
│   ├── story_reviewer.py
│   └── voice_narrator.py
│
├── assets/
│   └── images/
│
└── output/
```

## ⚙️ How It Works

### 1. Story Configuration

Users configure their story by selecting:

* Story theme
* Target age group
* Character name
* Character age
* Character appearance
* Moral lesson
* Number of pages

### 2. AI Story Generation

Google Gemini generates a structured children's story containing:

* Story title
* Character profile
* Moral lesson
* Page-wise story text
* Page-wise scene descriptions

### 3. Character Consistency

A character profile defines important visual attributes, including:

* Face
* Hair
* Eyes
* Skin tone
* Clothing
* Shoes
* Age
* Body proportions

These attributes are included in illustration prompts to help maintain a consistent character appearance across pages.

### 4. AI Illustration Generation

Hugging Face Inference Providers generate illustrations based on page-wise scene descriptions.

Example output files:

```text
character_reference.jpg
page_1.jpg
page_2.jpg
page_3.jpg
...
```

### 5. AI Story Reviewer

The AI Story Reviewer helps evaluate and improve generated stories by examining:

* Grammar and writing quality
* Age appropriateness
* Character consistency
* Story flow
* Moral clarity

It also provides feedback and AI-assisted story corrections.

### 6. AI Voice Narration

The voice narration feature converts story text into audio.

* Generate narration for a story
* Listen to the generated audio
* Download narration as an MP3 file
* Choose from supported languages: English, Hindi, and Marathi

The narration feature uses gTTS and requires an internet connection.

### 7. Story Library and Analytics

The application includes modules for story management and analytics, helping organize generated stories and analyze story-related information.

### 8. PDF Generation

ReportLab combines story text and illustrations into a final illustrated storybook PDF.

## 🔐 Environment Variables

Create a local `.env` file containing your API credentials:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_TEXT_MODEL=your_gemini_model_name

HF_TOKEN=your_huggingface_token
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
```

**Never upload your actual API keys or `.env` file to GitHub.**

For Streamlit Community Cloud deployment, configure credentials through the application's Secrets settings.

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aditya280505/AI-Storybook-Generator.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Storybook-Generator
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate.bat
```

### 5. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create the `.env` file in the project root and add your API credentials.

## ▶️ Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## 📖 Example

Example story configuration:

```text
Theme: Adventure
Age Group: 6–8
Character: Milo
Character Age: 7
Pages: 6
Moral: Friendship and kindness make every adventure better.
```

The application follows this workflow:

```text
Story Configuration
        ↓
AI Story Generation
        ↓
Character Profile
        ↓
Page-wise Scene Descriptions
        ↓
AI Illustrations
        ↓
Story Review and Corrections
        ↓
Voice Narration
        ↓
Story Library
        ↓
Final PDF Storybook
```

## 🧠 Prompt Engineering

The project uses structured prompts to improve:

* Character consistency
* Age appropriateness
* Visual style consistency
* Scene accuracy
* Story progression
* Reduction of unwanted text in images

Prompt iterations can be recorded through the prompt logging module.

Each log can contain:

```text
Page
Iteration
Prompt
Detected Issue
Solution
Timestamp
```

## ⚠️ Current Limitations

The illustration pipeline primarily uses prompt-based character consistency.

The character's visual attributes are repeatedly provided to the image model. This can improve consistency but does not guarantee identical character appearances across all illustrations.

Common image-generation challenges include:

* Variations in character appearance
* Changes in facial features
* Clothing inconsistencies
* Hand and finger generation errors
* Background variations
* Unwanted text appearing in images

These limitations are part of the project's prompt-engineering and model-evaluation considerations.

## 🎯 Problem Statement Coverage

| Requirement                              | Implementation                            |
| ---------------------------------------- | ----------------------------------------- |
| Choose a story theme                     | Streamlit input                           |
| Generate age-appropriate stories         | Google Gemini                             |
| Maintain character consistency           | Character profiles and structured prompts |
| Illustrate each page                     | Hugging Face image generation             |
| Record prompt iterations                 | Prompt logging module                     |
| Review and improve stories               | AI Story Reviewer                         |
| Generate story narration                 | gTTS                                      |
| Manage generated stories                 | Story Library module                      |
| Analyze story-related information        | Story Analytics module                    |
| Assemble the storybook                   | ReportLab                                 |
| Address image-generation inconsistencies | Prompt engineering and evaluation         |
| Maintain human editorial control         | Story review before finalization          |

## 👨‍💻 Author

**Aditya Borgaonkar**

B.Tech Computer Science Engineering — Artificial Intelligence & Analytics

* **GitHub:** https://github.com/aditya280505
* **LinkedIn:** https://linkedin.com/in/adityaborgaonkar280505/

## 📌 Project Type

**AI / Generative AI / NLP / Computer Vision / Full-Stack AI Application**

Developed as a college **Model Making** project for generating illustrated children's storybooks.
