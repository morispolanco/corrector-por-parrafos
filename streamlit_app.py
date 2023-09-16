# Import required Libraries
import streamlit as st
import docx
import openai
import pandas as pd
from docx import Document

# Define function to convert DOCX to pandas dataframe
def docx_to_df(file):
    doc = docx.Document(file)
    data = []
    for para in doc.paragraphs:
        data.append(para.text)
    df = pd.DataFrame(data, columns=["text"])
    return df

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key

# Streamlit App
st.title('DaVinci-003 Grammar and Style Correction for DOCX')

uploaded_file = st.file_uploader("Upload DOCX file", type='docx')

if uploaded_file is not None:
    df = docx_to_df(uploaded_file)
    corrected_document = Document() # This document will contain corrected text
    for index, row in df.iterrows():
        prompt=row['text']
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150
        )
        corrected_document.add_paragraph(response.choices[0].text.strip())
    corrected_document.save("corrected.docx")
    st.success('Done writing corrected document.')
    st.download_button('Download corrected DOCX', 'corrected.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
