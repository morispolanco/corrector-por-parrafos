# Import required Libraries
import streamlit as st
import docx
import openai
import pandas as pd
import spacy
from docx import Document

# Define function to convert DOCX to pandas dataframe
def docx_to_df(file):
    doc = docx.Document(file)
    data = []
    for para in doc.paragraphs:
        data.append(para.text)
    df = pd.DataFrame(data, columns=["texto"])
    return df

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key
# Streamlit App
st.title('Correción de gramática y estilo para DOCX usando DaVinci-003')

uploaded_file = st.file_uploader("Sube un archivo DOCX", type='docx')

# Load Spacy model
nlp = spacy.load("es_core_news_sm")

if uploaded_file is not None and st.button('Corregir'):
    with st.spinner("Corrigiendo..."):
        df = docx_to_df(uploaded_file)
        corrected_document = Document() # Este documento contiene el texto corregido
        for index, row in df.iterrows():
            doc = nlp(row['texto'])
            sentences = [sent.string.strip() for sent in doc.sents]
            for sentence in sentences:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=sentence,
                    temperature=0.5,
                    max_tokens=100 
                )
                corrected_document.add_paragraph(response.choices[0].text.strip())
        corrected_document.save("corrected.docx")
        st.success('Se ha completado la corrección del documento.')
        st.download_button('Descarga el documento corregido DOCX', 'corrected.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
