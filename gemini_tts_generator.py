import io
import os
import wave
from typing import List

import streamlit as st
from google import genai
from google.genai import types


APP_TITLE = "Gemini TTS Generator"
MODEL_OPTIONS = {
    "Fast / cheaper": "gemini-2.5-flash-preview-tts",
    "Higher quality": "gemini-2.5-pro-preview-tts",
}
VOICE_OPTIONS: List[str] = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede",
    "Callirrhoe", "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba",
    "Despina", "Erinome", "Algenib", "Rasalgethi", "Laomedeia", "Achernar",
    "Alnilam", "Schedar", "Gacrux", "Pulcherrima", "Achird", "Zubenelgenubi",
    "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
]

st.set_page_config(page_title=APP_TITLE, page_icon="🔊", layout="wide")
st.title(APP_TITLE)
st.caption("An ElevenLabs-style text-to-speech UI using the Gemini API.")

@st.cache_resource
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=api_key)

def pcm_to_wav_bytes(pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(rate)
        wav_file.writeframes(pcm)
    buffer.seek(0)
    return buffer.read()

def build_prompt(style: str, text: str) -> str:
    style = style.strip()
    text = text.strip()
    if not style:
        return text
    return f"Read this exactly in the following style: {style}\n\nText: {text}"

def generate_speech(model: str, voice_name: str, prompt: str) -> bytes:
    client = get_client()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                )
            ),
        ),
    )

    pcm_data = response.candidates[0].content.parts[0].inline_data.data
    if not pcm_data:
        raise RuntimeError("No audio data returned by the API.")

    return pcm_to_wav_bytes(pcm_data)

left, right = st.columns([1, 1])

with left:
    st.subheader("Voice settings")
    model_label = st.selectbox("Model", list(MODEL_OPTIONS.keys()), index=0)
    model_name = MODEL_OPTIONS[model_label]
    voice_name = st.selectbox("Voice", VOICE_OPTIONS, index=3)
    style_prompt = st.text_area(
        "Voice direction",
        value="Warm, natural, clear, and slightly cinematic.",
        height=110,
    )
    speaking_language = st.text_input("Language hint (optional)", value="Bangla")

with right:
    st.subheader("Script")
    text_input = st.text_area(
        "Text to convert",
        value="আসসালামু আলাইকুম। আজকের ভিডিওতে আমরা এমন একটি ঘটনা শুনব, যা প্রথম থেকে শেষ পর্যন্ত আপনার মনোযোগ ধরে রাখবে।",
        height=260,
    )
    final_style = style_prompt.strip()
    if speaking_language.strip():
        final_style = f"Speak in {speaking_language.strip()}. {final_style}".strip()

    final_prompt = build_prompt(final_style, text_input)

st.divider()

if st.button("Generate speech", type="primary", use_container_width=True):
    if not text_input.strip():
        st.error("Please enter some text first.")
    else:
        try:
            with st.spinner("Generating audio..."):
                wav_bytes = generate_speech(model_name, voice_name, final_prompt)

            st.success("Audio generated successfully.")
            st.audio(wav_bytes, format="audio/wav")
            st.download_button(
                label="Download WAV",
                data=wav_bytes,
                file_name="gemini_tts_output.wav",
                mime="audio/wav",
                use_container_width=True,
            )
        except Exception as error:
            st.error(str(error))
