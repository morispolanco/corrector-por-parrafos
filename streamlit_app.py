# Import required Libraries
import streamlit as st
import docx
import openai
import csv
from docx import Document

# Define function to convert DOCX to CSV
def docx_to_csv(file, csv_file):
    doc = docx.Document(file)
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for para in doc.paragraphs:
            writer.writerow([para.text])

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key

# Streamlit App
st.title('DaVinci-003 Grammar and Style Correction for DOCX')

uploaded_file = st.file_uploader("Upload DOCX file", type='docx')

if uploaded_file is not None and st.button('Corregir'):
    with st.spinner("Corrigiendo..."):
        # Converting DOCX to CSV
        csv_file = 'input.csv'
        docx_to_csv(uploaded_file, csv_file)
        
        corrected_document = Document() # This document will contain corrected text
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=row[0],
                    temperature=0.5,
                    max_tokens=100 
                )
                corrected_document.add_paragraph(response.choices[0].text.strip())
        corrected_document.save("corrected.docx")
        st.success('Se ha completado la corrección del documento.')
        st.download_button('Descarga el documento corregido DOCX', 'corrected.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
