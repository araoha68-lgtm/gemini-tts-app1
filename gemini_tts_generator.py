import streamlit as st
import os
from google import genai
from google.genai import types

# Page config
st.set_page_config(page_title="Gemini TTS", page_icon="🔊")

st.title("🔊 Gemini Text to Speech")

# Get API key from Streamlit secrets
api_key = os.getenv("GEMINI_API_KEY")

# Input text
text = st.text_area("Enter text to convert", height=200)

# Button
if st.button("Generate speech"):
    if not api_key:
        st.error("GEMINI_API_KEY is not set.")
    elif not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=text
            )

            # Show text response
            st.success("Generated Text Output:")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
