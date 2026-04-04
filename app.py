import streamlit as st
import requests
import os

st.title("AI Chat")

api_key = os.getenv("HF_API_KEY")

prompt = st.text_area("Ask something")

if st.button("Send"):
    if not api_key:
        st.error("HF_API_KEY missing")
    elif not prompt.strip():
        st.warning("Enter a prompt")
    else:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"inputs": prompt}
        )
        st.write(response.json())
