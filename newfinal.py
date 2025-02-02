import streamlit as st
import google.generativeai as genai
import speech_recognition as sr  # Voice Input
import cv2  # Camera Integration
import easyocr  # OCR for Handwritten Text Recognition (Replaced Tesseract)
import sqlite3  # User authentication & storage
from uuid import uuid4  # Unique ID for versioning

# --- API CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyDOvM48IMxod_4SvEttajKXcVDblmKHyPk"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# --- DATABASE FOR USER AUTHENTICATION ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# --- INITIALIZE DATABASE ---
init_db()

# --- USER AUTHENTICATION PAGE ---
def login_page():
    st.markdown("""
        <div style='text-align:center;'>
            <h1 style='color:rgb(206, 191, 79); font-family: Roboto; font-size: 48px;'>UwU Code Generator</h1>
            <h3 style='color: #666;'>Unlock the magic of UwU coding!</h3>
            <p style='color: #888;'>Login or Register to start your UwU coding journey!</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://cdn.pixabay.com/photo/2016/12/07/15/50/code-1891656_960_720.jpg", use_container_width=True)
        st.subheader("🔑 Welcome to UwU Code Generator X")
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        login = st.button("🔓 Login", use_container_width=True)
        register = st.button("📝 Register", use_container_width=True)
        
        if login:
            if login_user(username, password):
                st.session_state["authenticated"] = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Invalid username or password")
        
        if register:
            if register_user(username, password):
                st.success("✅ Registered successfully! Please login.")
            else:
                st.error("❌ Username already exists!")

# --- CODE GENERATION FUNCTION ---
def generate_code_in_language(prompt, language):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Write {language} code for: {prompt}")
        return response.text
    except Exception as e:
        return f"Error generating code: {str(e)}"

# --- MAIN APP ---
def main():
    st.markdown("""
        <style>
            .stButton button { 
                background-color: #ff7f50;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    if "authenticated" not in st.session_state:
        login_page()
        return
    
    st.markdown("""
        <h1 style='text-align: center; color: #ff7f50; font-family: Arial, sans-serif; font-size: 48px;'>UwU Code Generator</h1>
    """, unsafe_allow_html=True)
    
    language_choice = st.selectbox("🌍 Choose Programming Language", ["UwU", "Python", "JavaScript", "Rust", "C++", "C++ to UwU"], index=0)
    user_prompt = st.text_area("📝 Describe your vision for UwU code 🚀", placeholder="e.g. Print 'Hello, World!' in UwU language", height=150)
    
    col1, col2 = st.columns(2)
    
    # --- Voice Input ---
    with col1:
        if st.button("🎙 Voice Input"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("🎙 Speak now...")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio)
                    user_prompt += " " + text
                    st.text_area("📝 Updated Prompt from Voice:", user_prompt, height=150)
                except:
                    st.error("❌ Speech recognition failed")
    
    # --- Image Text Extraction (OCR) ---
    with col2:
        if st.button("📸 Capture Photo"):
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if ret:
                st.image(frame, channels="BGR", caption="📸 Captured Image")
                try:
                    reader = easyocr.Reader(["en"])  # Using EasyOCR
                    text = reader.readtext(frame, detail=0)  # Extracting text
                    extracted_text = " ".join(text)  # Converting list to string
                    user_prompt += " " + extracted_text
                    st.text_area("📝 Extracted Text from Image:", user_prompt, height=150)
                except Exception as e:
                    st.error(f"❌ OCR Failed: {e}")
            else:
                st.error("❌ Failed to capture image")
    
    # --- Code Generation ---
    if st.button("✨ Generate Code!"):
        if user_prompt:
            generated_code = generate_code_in_language(user_prompt, language_choice)
            st.code(generated_code, language=language_choice.lower(), line_numbers=True)
        else:
            st.warning("⚠ Please enter a description!")
    
    # --- Footer ---
    st.markdown("""
        <div style="text-align:center; padding-top:20px;">
            <b>Made with ❤ for UwU lovers! By Nitish, Shivam, Shubham, Sourish ✨</b>
        </div>
    """, unsafe_allow_html=True)

# ✅ FIX: Corrected the syntax error in the if __name__ == "__main__": line
if __name__ == "__main__":
    main()
