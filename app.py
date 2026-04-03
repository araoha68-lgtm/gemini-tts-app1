import streamlit as st
import os
import google.generativeai as genai

st.title("Gemini App")

# Load API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key missing")
else:
    genai.configure(api_key=api_key)

text = st.text_area("Enter text")

if st.button("Generate"):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(text)
        st.write(response.text)
    except Exception as e:
        st.error(e)
