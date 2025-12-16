import os
import sys
from google import genai
from google.genai.errors import APIError
from database import create_db_and_tables, add_student, get_all_students, save_lesson, get_db
from models import Student

# --- LLM Integration Setup ---

# The client will automatically pick up the GEMINI_API_KEY environment variable.
try:
    AI_CLIENT = genai.Client() #
    AI_MODEL = 'gemini-2.5-flash'
except Exception as e:
    print(f"Error initializing AI client: {e}")
    print("Please ensure the GEMINI_API_KEY environment variable is set correctly.")
    sys.exit(1)


# --- 2. Lesson Generation Function ---

def generate_lesson(topic: str, student: Student, client: genai.Client):
    """
    Generates a personalized lesson using the Gemini API.
    """
    accommodations = f"""
    - Preferred Learning Style: {student.preferred_learning_style}
    - Known Barriers: {student.known_barriers} 
    - Interests/Motivators: {student.interests}
    """
    
    prompt = f"""
    You are an expert inclusive education specialist designing a short, highly personalized lesson.
    
    **Task:** Create a 5-minute mini-lesson on the topic: "{topic}".
    
    **Student Profile (Adapt to these needs):**
    {accommodations}
    
    **Lesson Requirements:**
    1. **Format:** Use clear, simple, bolded markdown headings.
    2. **Tone:** Encouraging, clear, and direct.
    3. **Structure:**
        * **Objective:** State ONE simple, concrete goal.
        * **Concept Breakdown:** Break the main concept into 3-5 short, sequential steps. Use bullet points or numbered lists for clarity.
        * **Analogy/Example:** Integrate the student's **Interests** (e.g., if their interest is 'Space', use a space analogy).
        * **Activity:** Suggest one short, kinesthetic or visual check-for-understanding activity (e.g., 'Draw it,' 'Build it,' 'Say it out loud').
    4. **Accessibility:** Ensure the language uses short sentences and avoids overly complex vocabulary to support students with reading difficulties.
    """
    
    print(f"\n--- Generating Lesson for {student.name} on '{topic}' ---")
    
    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"**[AI Error]**: Could not generate content. Check API key and quota. Error: {e}"
    except Exception as e:
        return f"**[General Error]**: An unexpected error occurred: {e}"


# --- 4. Test Script (Execute to see the result!) ---

if __name__ == "__main__":
    
    # 1. Ensure DB and Sample Data exist
    create_db_and_tables()
    db = next(get_db())
    
    students = get_all_students(db)
    if not students:
        print("No students found. Run database.py directly to add sample students, then re-run this script.")
        db.close()
        sys.exit(1)

    # 2. Select a sample student and topic
    # We will pick the first sample student (Liam)
    sample_student: Student = students[0]
    sample_topic = "How Photosynthesis Works" 

    # 3. Generate the lesson
    lesson_content = generate_lesson(sample_topic, sample_student, AI_CLIENT)
    
    # 4. Save and Print the result
    if not lesson_content.startswith("**[AI Error]**"):
        saved_lesson = save_lesson(db, sample_student.id, sample_topic, lesson_content)
        
        print("\n" + "="*50)
        print(f"✅ Lesson Saved Successfully!")
        print(f"   Student: {saved_lesson.student.name}")
        print(f"   Topic: {saved_lesson.topic}")
        print(f"   Lesson ID: {saved_lesson.id}")
        print("="*50)
        
        print("\n*** GENERATED LESSON CONTENT (Markdown Preview) ***\n")
        print(lesson_content)
        print("\n************************************************\n")
    else:
        print(f"\n❌ Generation failed: {lesson_content}")

    # 5. Check if the lesson is in the database
    print(f"Total lessons saved for {sample_student.name}: {len(sample_student.lessons)}")
    
    db.close()