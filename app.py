import spacy
from annotated_text import annotated_text
import requests
import streamlit as st
#from streamlit_lottie import st_lottie
from PIL import Image
#from streamlit_option_menu import option_menu

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")



# side bar menu
with st.sidebar:
#     selected = option_menu(
#         menu_title="Main Menu",
#         options=["home", "Projects", "Work Experience", "Contact"])

# if selected == "home":
    st.title(f'Welcome to NER_Anonymizer web_page ')


@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_models():
    french_model = spacy.load("./models/fr/")
    english_model = spacy.load("./models/en/")
    models = {"en": english_model, "fr": french_model}
    return models


def process_text(doc, selected_entities, anonymize=False):
    tokens = []
    for token in doc:
        if (token.ent_type_ == "PERSON") & ("PER" in selected_entities):
            tokens.append((token.text, "Person", "#faa"))
        elif (token.ent_type_ in ["GPE", "LOC"]) & ("LOC" in selected_entities):
            tokens.append((token.text, "Location", "#fda"))
        elif (token.ent_type_ == "ORG") & ("ORG" in selected_entities):
            tokens.append((token.text, "Organization", "#afa"))
        else:
            tokens.append(" " + token.text + " ")

    if anonymize:
        anonmized_tokens = []
        for token in tokens:
            if type(token) == tuple:
                anonmized_tokens.append(("X" * len(token[0]), token[1], token[2]))
            else:
                anonmized_tokens.append(token)
        return anonmized_tokens

    return tokens


models = load_models()

selected_language = st.sidebar.selectbox("Language please", options=["en", "fr"])
selected_entities = st.sidebar.multiselect(
    "Select the entities you want to detect",
    options=["LOC", "PER", "ORG"],
    default=["LOC", "PER", "ORG"],
)
selected_model = models[selected_language]

text_input = st.text_area("Text to anonymize:")

uploaded_file = st.file_uploader("want to upload any file? ", type=["doc", "docx", "pdf", "txt"])
if uploaded_file is not None:
    text_input = uploaded_file.getvalue()
    text_input = text_input.decode("utf-8")

anonymize = st.checkbox("Anonymize")
doc = selected_model(text_input)
tokens = process_text(doc, selected_entities)

annotated_text(*tokens)

if anonymize:
    st.markdown("**Your Anonymized text**")
    st.markdown("---")
    anonymized_tokens = process_text(doc, selected_entities, anonymize=anonymize)
    annotated_text(*anonymized_tokens)
