import streamlit as st
import time
import os
import requests

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Updated import

# Load environment variables from .env file
load_dotenv()


# Initialize ChatOpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')
chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

#lottie function
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_url_lang = "https://lottie.host/adb921b3-5206-4334-b416-b3e24447ddb0/3eEcVIYvkr.json"
lottie_lang = load_lottieurl(lottie_url_lang)



st.set_page_config(page_title="Transl8")
# Streamlit UI
st.title("TRANSL8")
st_lottie(lottie_lang, key="lang", quality='high' ,height= 300 ,width=300)
st.subheader("Translation made simple")
st.write("Conquer language barriers in seconds! Drag and drop your Text files, and our AI whiz, OpenAI, will translate them with lightning speed.")



lottie_url_loading = "https://lottie.host/bb37ef5a-c0fa-4403-85c0-4dfdbdc8f0a0/cyDBwsjXwI.json"

lottie_loading = load_lottieurl(lottie_url_loading)





main_placeholder = st.empty()

language_codes = {
  "en": "English",
  "bg": "Bulgarian",
  "hr": "Croatian",
  "cs": "Czech",
  "da": "Danish",
  "nl": "Dutch",
  "et": "Estonian",
  "fi": "Finnish",
  "fr": "French",
  "de": "German",
  "el": "Greek",
  "hu": "Hungarian",
  "id": "Indonesian",
  "it": "Italian",
  "kk": "Kazakh",
  "lv": "Latvian",
  "lt": "Lithuanian",
  "nb": "Norwegian Bokmål",
  "pl": "Polish",
  "pt": "Portuguese",
  "ro": "Romanian",
  "ru": "Russian",
  "sr": "Serbian",
  "sk": "Slovak",
  "sl": "Slovenian",
  "es": "Spanish",
  "sv": "Swedish",
  "tr": "Turkish",
  "vi": "Vietnamese"
}


# Create a sidebar

with st.sidebar:
    st.title("File Upload")

    # Add file uploader to the sidebar
    uploaded_file = st.file_uploader("Upload text file", type=["txt"])

    
    if uploaded_file :
        Next_url_clicked = st.sidebar.button("Next")
        
        try:
            with open(uploaded_file.name, 'r', encoding='utf-8') as f:
                content = f.read()
                st.success("File contents loaded successfully")

            
            
            if Next_url_clicked:
                st.success("select the language in the language section")
            
            r_splitter = RecursiveCharacterTextSplitter(
                separators = ["\n\n" , "\n", " ", "."],
                chunk_size = 300,
                chunk_overlap = 0
                )
            chunks = r_splitter.split_text(content)
            


        except Exception as e:
            st.error(f"Error loading file: {e}")




# Translation prompt template (flexible for target language)
translation_prompt = ChatPromptTemplate.from_messages([
    system_message := " Assuming you are a professional in translation give me accurate translation in target language, Translate the following text to:",
    human_language := "{target_language}",  # Placeholder for target language
    human_message := "{text}"  # Placeholder for text chunks
])

def translate_chunks(chunks, target_language):
    translated_text = []
    if target_language == "English":  # Check if target is English
        for chunk in chunks:
              # Display original text for English to English
            translated_text.append(chunk)
    else:
        for chunk in chunks:
            formatted_prompt = translation_prompt.format_prompt(
                target_language=target_language, text=chunk
            )
            
            response = chat.invoke(formatted_prompt.to_messages())
            translated_chunk = response.content.strip()
            translated_text.append(translated_chunk)
    return " ".join(translated_text)
    





Next_url_clicked_obj = True

    

if Next_url_clicked_obj:
    # Language selection and process button in the main area
    st.header("LANGUAGE SELECTION AREA")
    selected_languages = st.multiselect("select the languages to which you want to translate",placeholder = "Choose atleast one target language",options=list(language_codes.values()))  # Use language code keys
    
    

    translated_texts = {}
    if selected_languages:
        if uploaded_file:
            for lang_code in selected_languages:
                
                translated_text = translate_chunks(chunks, lang_code)
                translated_texts[lang_code] = translated_text
        else:
            st.error("Please upload your text file")

        # Display download buttons for each translated language
        # Display animation once before iterating over selected languages
        with st_lottie_spinner(lottie_loading, key="loading", height=200 , width=200):
            time.sleep(3)  # Simulate loading

# Iterate over selected languages
        for lang_code, translated_text in translated_texts.items():
            language_name = language_codes.get(lang_code, lang_code)  # Use full name if available
            download_button_label = f"{language_name} Text Download"
            unique_key = f"loading_{lang_code}"
            st.download_button(label=download_button_label, data=translated_text, file_name=f"{language_name}.txt")


            
            

        

    
















