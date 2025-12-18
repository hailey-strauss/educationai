import os
import streamlit as st
from google import genai
from dotenv import load_dotenv  
load_dotenv()                   
from google.genai.errors import APIError

# --- Page Configuration ---
st.set_page_config(page_title="Personalized Lesson Creator", layout="wide")

# --- AI Client Setup ---
# It's best practice to use st.secrets or environment variables
gemini_key = os.getenv("GEMINI_API_KEY")

def get_ai_client():
    if not gemini_key:
        st.error("Missing GEMINI_API_KEY. Please set it in your environment.")
        return None
    return genai.Client(api_key=gemini_key)

AI_MODEL = 'gemini-2.0-flash'

# --- UI Layout ---
st.title("🎓 AI Lesson Personalizer")
st.write("Turn any standard lesson into a custom experience based on student interests.")

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("Input Details")
    # Input: Student Interest Information
    student_interests = st.text_input(
        "Student Interests & Motivators", 
        placeholder="e.g. Minecraft, NASA, basketball, drawing..."
    )
    
    # Input: The Lesson Content
    base_lesson = st.text_area(
        "Current Lesson Plan or Topic", 
        height=300,
        placeholder="Paste the lesson content you want to transform here..."
    )
    
    generate_btn = st.button("Generate Tailored Lesson", type="primary")

with col2:
    st.subheader("Tailored Output")
    
    if generate_btn:
        if not student_interests or not base_lesson:
            st.warning("Please provide both student interests and a lesson plan.")
        else:
            client = get_ai_client()
            if client:
                with st.spinner("Injecting interests into lesson..."):
                    # Prompt Construction (Injection)
                    prompt = f"""
                    You are an expert inclusive education specialist.
                    
                    **Target Interest/Motivator:** {student_interests}
                    
                    **Original Content:**
                    {base_lesson}
                    
                    **Task:** Rewrite the original content into a 5-minute mini-lesson tailored specifically to the interests provided.
                    
                    **Requirements:**
                    1. **Analogy/Example:** You MUST use the interest ({student_interests}) as the primary way to explain the concept.
                    2. **Format:** Use bolded markdown headings.
                    3. **Structure:**
                        * **Objective:** One concrete goal.
                        * **Concept Breakdown:** 3-5 short steps.
                        * **Activity:** One kinesthetic or visual check-for-understanding.
                    4. **Tone:** Clear, direct, and highly encouraging.
                    """

                    try:
                        response = client.models.generate_content(
                            model=AI_MODEL,
                            contents=prompt
                        )
                        # Display the result
                        st.markdown(response.text)
                        
                        # Add a download option for the teacher
                        st.download_button(
                            label="Download Lesson (.txt)",
                            data=response.text,
                            file_name="tailored_lesson.txt",
                            mime="text/plain"
                        )
                    except APIError as e:
                        st.error(f"API Error: {e}")
                    except Exception as e:
                        st.error(f"Error: {e}")
    else:
        st.info("Your tailored lesson will appear here once you click 'Generate'.")