# AI Lesson Tailor

An intelligent tool designed for educators to instantly personalize lesson plans. By combining a student's specific interests with standard curriculum content, this application uses **Google Gemini AI** to generate highly engaging, inclusive mini-lessons.

---

## Features

- **Interest Injection:** Seamlessly weaves student motivators (e.g., Minecraft, Space, Sports) into educational content.
- **Inclusive Design:** Focuses on clear objectives, concept breakdowns, and kinesthetic activities.
- **Streamlit Interface:** A clean, easy-to-use web interface for inputting data and viewing results.
- **One-Click Download:** Export your tailored lesson plan as a `.txt` file.

---

## Installation (macOS)

Follow these steps to set up the project on your Mac:

### 1. Clone or Open the Project

Navigate to your project folder in the terminal:

```bash
cd educationai
```

### 2. Install Dependencies

Use python3 to install the required libraries:

Create a file named .env in the root folder and add your Gemini API key:

Code snippet
GEMINI_API_KEY=your_actual_key_here

### How to Run

To launch the app, run the following command in your terminal:

Bash
python3 -m streamlit run lesson_generator.py
Once running, the app will automatically open in your default browser at http://localhost:8501.

Usage Guide
Enter Interests: Input what the student is passionate about (e.g., "Enjoys building in Roblox and playing soccer").

Paste Lesson: Paste a standard lesson plan or a specific topic (e.g., "The Water Cycle").

Generate: Click "Generate Tailored Lesson".

Review & Save: View the AI-generated lesson on the right side of the screen and download it if needed.

Tech Stack
Frontend: Streamlit

AI Model: Google Gemini 2.0 Flash

Language: Python 3.x
