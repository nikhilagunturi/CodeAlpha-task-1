import os
import time

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered"
)


st.title("Language Translation Tool")
st.write("Translate text between different languages using Gemini AI.")


languages = [
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Azerbaijani",
    "Basque",
    "Belarusian",
    "Bengali",
    "Bosnian",
    "Bulgarian",
    "Catalan",
    "Chinese",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Estonian",
    "Filipino",
    "Finnish",
    "French",
    "Georgian",
    "German",
    "Greek",
    "Gujarati",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Kannada",
    "Kazakh",
    "Khmer",
    "Korean",
    "Kyrgyz",
    "Lao",
    "Latvian",
    "Lithuanian",
    "Malay",
    "Malayalam",
    "Marathi",
    "Mongolian",
    "Nepali",
    "Norwegian",
    "Odia",
    "Persian",
    "Polish",
    "Portuguese",
    "Punjabi",
    "Romanian",
    "Russian",
    "Serbian",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Swahili",
    "Swedish",
    "Tamil",
    "Telugu",
    "Thai",
    "Turkish",
    "Turkmen",
    "Ukrainian",
    "Urdu",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Zulu"
]


if "history" not in st.session_state:
    st.session_state.history = []


source_language = st.selectbox(
    "Select source language",
    languages
)

target_language = st.selectbox(
    "Select target language",
    languages,
    index=1
)

text = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type your text here..."
)


col1, col2 = st.columns(2)

with col1:
    translate_button = st.button(
        "Translate",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "Clear",
        use_container_width=True
    )


if clear_button:
    st.rerun()


if translate_button:

    if not text.strip():
        st.warning("Please enter some text.")

    elif source_language == target_language:
        st.info("Source and target languages are the same.")
        st.write(text)

    else:

        prompt = f"""
Translate the following text from {source_language} to {target_language}.

Provide two versions:

1. Romanized:
Write the translation using English/Roman letters where applicable.

2. Native Script:
Write the translation using the target language's native writing system.

IMPORTANT:
- Use natural, casual, everyday language.
- Preserve the exact meaning.
- Do not add explanations.
- Do not add quotation marks.
- Return ONLY these two lines.

Format exactly:

Romanized: <translation>
Native Script: <translation>

Text:
{text}
"""

        try:

            with st.spinner("Translating..."):

                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt
                )

            translated_text = response.text.strip()

            romanized = ""
            native_script = ""

            for line in translated_text.splitlines():

                if line.startswith("Romanized:"):
                    romanized = line.replace(
                        "Romanized:",
                        "",
                        1
                    ).strip()

                elif line.startswith("Native Script:"):
                    native_script = line.replace(
                        "Native Script:",
                        "",
                        1
                    ).strip()

            st.subheader("Translation")

            st.markdown(
                f"**Romanized:** {romanized}"
            )

            st.markdown(
                f"**Native Script:** {native_script}"
            )

            full_translation = (
                f"Romanized: {romanized}\n"
                f"Native Script: {native_script}"
            )

            st.code(
                full_translation,
                language=None
            )

            st.session_state.history.insert(
                0,
                {
                    "source": text,
                    "source_language": source_language,
                    "target_language": target_language,
                    "romanized": romanized,
                    "native_script": native_script
                }
            )

        except Exception as e:

            st.error(
                f"Translation failed: {e}"
            )


if st.session_state.history:

    st.divider()

    st.subheader("Translation History")

    for item in st.session_state.history:

        with st.expander(
            f"{item['source_language']} → {item['target_language']}"
        ):

            st.write(
                f"Original: {item['source']}"
            )

            st.write(
                f"Romanized: {item['romanized']}"
            )

            st.write(
                f"Native Script: {item['native_script']}"
            )



