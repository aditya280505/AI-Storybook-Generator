# 📚 AI-Generated Children's Storybook

> An AI-powered web application that automatically creates illustrated children's storybooks from user-provided themes, characters, age groups, and moral lessons.

### 🚀 Live Demo

**[▶️ Try the AI Storybook Generator](http://ai-storybook-generator-jfs5ycyxu6dkga23dtyyfw.streamlit.app/)**

### 📌 Project Overview

The application uses **Google Gemini** for story generation, **Hugging Face Inference Providers** for AI-generated illustrations, and **ReportLab** to assemble the final storybook into a PDF.

---

## 🚀 Features

* ✨ AI-generated children's stories
* 🎨 AI-generated page illustrations
* 👦 Consistent character description across pages
* 🧒 Age-appropriate story generation
* 📖 Multi-page storybook creation
* 💡 Moral-based storytelling
* 📝 Page-wise scene descriptions
* 🔄 Prompt iteration and logging
* 👀 Human review before finalization
* 📄 Automatic PDF storybook generation
* 🌐 Streamlit-based interactive web interface


---

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
AI Illustrations
  ↓
Human Review
  ↓
ReportLab PDF Generator
  ↓
📖 Final Storybook PDF
```

---

## 🛠️ Technologies Used

| Technology                       | Purpose                                |
| -------------------------------- | -------------------------------------- |
| Python                           | Core programming language              |
| Streamlit                        | Web application interface              |
| Google Gemini API                | Story and content generation           |
| Hugging Face Inference Providers | AI image generation                    |
| FLUX.1-schnell                   | Storybook illustration generation      |
| Pillow                           | Image processing                       |
| ReportLab                        | PDF generation                         |
| JSON                             | Structured story and prompt data       |
| python-dotenv                    | Environment variable management        |
| Git & GitHub                     | Version control and repository hosting |

---

## 📂 Project Structure

```text
AI_STORYBOOK/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── story_generator.py
│   ├── image_generator.py
│   ├── pdf_generator.py
│   └── prompt_logger.py
│
├── assets/
│   └── images/
│
└── output/
```

---

## ⚙️ How It Works

### 1. Story Configuration

The user selects:

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
* Moral
* Page-wise story text
* Page-wise scene descriptions

### 3. Character Consistency

A fixed character profile is created containing important visual attributes such as:

* Face
* Hair
* Eyes
* Skin tone
* Clothing
* Shoes
* Age
* Body proportions

These attributes are repeatedly included in illustration prompts to improve visual consistency.

### 4. AI Illustration Generation

Hugging Face Inference Providers are used to generate illustrations from the page scene descriptions.

The application generates:

```text
character_reference.jpg
page_1.jpg
page_2.jpg
page_3.jpg
...
```

### 5. Human Editorial Review

Generated stories and illustrations can be reviewed before creating the final book.

This keeps the human in control of:

* Story quality
* Visual quality
* Character consistency
* Age appropriateness
* Final selection

### 6. PDF Generation

ReportLab combines the generated text and illustrations into a final illustrated storybook PDF.

---

## 🔐 Environment Variables

Create a `.env` file locally:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_TEXT_MODEL=gemini-3.5-flash-lite

HF_TOKEN=YOUR_HUGGINGFACE_TOKEN
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
```

**Never commit API keys to GitHub.**

For Streamlit Cloud deployment, add these values through:

```text
Streamlit Cloud
→ Manage App
→ Settings
→ Secrets
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/aditya280505/AI-Storybook-Generator.git
```

Navigate to the project:

```bash
cd AI-Storybook-Generator
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start Streamlit:

```bash
python -m streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

---

## 📖 Example

Example configuration:

```text
Theme: Adventure
Age Group: 6–8
Character: Milo
Character Age: 7
Pages: 6
Moral: Friendship and kindness make every adventure better.
```

The system generates:

```text
Story
   ↓
Character Profile
   ↓
Scene Descriptions
   ↓
Character Reference
   ↓
Page Illustrations
   ↓
Final PDF Storybook
```

---

## 🧠 Prompt Engineering

The project uses structured prompts to improve:

* Character consistency
* Age appropriateness
* Visual style consistency
* Scene accuracy
* Story progression
* Removal of unwanted text from images

Prompt iterations can be recorded using the prompt logging module.

Each log can contain:

```text
Page
Iteration
Prompt
Detected Issue
Solution
Timestamp
```

---

## ⚠️ Current Limitation

The current illustration pipeline primarily uses **prompt-based character consistency**.

The character's fixed visual attributes are repeatedly provided to the image model. This improves consistency, but it is not equivalent to advanced reference-image conditioning.

Common image-generation challenges include:

* Character appearance variations
* Different facial features
* Clothing inconsistencies
* Hand and finger errors
* Background variations
* Unwanted text appearing in images

These limitations are documented as part of the project's prompt-engineering and model-evaluation process.

---

## 🎯 Problem Statement Coverage

This project addresses the following requirements:

| Requirement                      | Implementation                         |
| -------------------------------- | -------------------------------------- |
| Choose theme                     | Streamlit input                        |
| Generate age-appropriate story   | Google Gemini                          |
| Consistent characters            | Character profile + structured prompts |
| Illustrate each page             | Hugging Face image generation          |
| Prompt iterations                | Prompt logging module                  |
| Assemble storybook               | ReportLab                              |
| Character consistency reflection | Prompt-based consistency               |
| Hands/text-in-image challenges   | Negative prompt instructions           |
| Human editorial control          | Review before PDF generation           |

---

## 👨‍💻 Author

**Aditya Borgaonkar**
B.Tech Computer Science Engineering — Artificial Intelligence & Analytics

* **GitHub:** https://github.com/aditya280505
* **LinkedIn:** https://linkedin.com/in/adityaborgaonkar280505/

---

⭐ If you found this project interesting, feel free to explore the repository and try the **Live Demo**!
## 👨‍💻 Author

**Aditya Borgaonkar**

B.Tech Computer Science Engineering
Artificial Intelligence & Analytics

GitHub:
https://github.com/aditya280505

---

## 📌 Project Type

**AI / Generative AI / NLP / Computer Vision / Full-Stack AI Application**

Built as a college **Model Making** project for an AI-generated children's storybook.
