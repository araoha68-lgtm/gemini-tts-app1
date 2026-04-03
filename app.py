import streamlit as st
import os
from google.genai import Client

st.title("Gemini App")

api_key = os.getenv("GEMINI_API_KEY")

text = st.text_area("Enter text")

if st.button("Generate"):
    if not api_key:
        st.error("API key missing")
    else:
        try:
            client = Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=text
            )
            st.write(response.text)
        except Exception as e:
            st.error(e)
