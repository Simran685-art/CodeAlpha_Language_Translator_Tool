import streamlit as st
from deep_translator import GoogleTranslator
import pyttsx3
import os

# Set page layout and configuration
st.set_page_config(
    page_title="Advanced Language Translator",
    page_icon="🌍",
    layout="wide"
)

# Initialize session state for translation history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🌍 Advanced Language Translation Tool")
st.write("Translate text between multiple languages with AI support.")

# Supported languages dictionary
languages = {
    "English": "en",
    "Hindi": "hi",
    "Punjabi": "pa",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru",
    "Arabic": "ar"
}

# Sidebar configuration for history tracking
st.sidebar.title("📜 Translation History")

if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []

for item in reversed(st.session_state.history):
    st.sidebar.write(item)

# UI layout split into two columns for dropdowns
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1  # Default target set to Hindi
    )

# Input text area
text = st.text_area(
    "Enter Text",
    height=150
)

# Live counter for characters and words
characters = len(text)
words = len(text.split())

st.write(f"📝 Characters: {characters}")
st.write(f"📖 Words: {words}")

# Translation execution block
if st.button("🚀 Translate"):
    if text.strip():
        try:
            # Map selected language code directly
            detected_code = languages[source_lang]

            # Translation process using GoogleTranslator API
            translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

            st.success("✅ Translation Completed")
            st.info(f"🌐 Selected Language Code: {detected_code}")

            st.subheader("Translated Text")
            st.write(translated)

            # Append tracking info to session history
            st.session_state.history.append(
                f"{source_lang} ➜ {target_lang}: {translated}"
            )

            # Fast Offline Text-to-Speech using pyttsx3
            engine = pyttsx3.init()
            audio_file = "translation.mp3"
            
            # Save to file directly and play via streamlit
            engine.save_to_file(translated, audio_file)
            engine.runAndWait()

            if os.path.exists(audio_file):
                with open(audio_file, "rb") as audio:
                    st.audio(audio.read())

            # Provide file download option for translated text
            st.download_button(
                "📥 Download Translation",
                translated,
                file_name="translation.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error executing translation: {e}")
    else:
        st.warning("Please enter some text to translate.")