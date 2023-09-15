import streamlit as st
import pandas as pd
import docx
from docx import Document
import openai

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Ingresa tu clave de API de OpenAI", type="password")

if not api_key:
    st.warning("Por favor, ingresa una clave de API válida para continuar.")
else:
    openai.api_key = api_key

def correct_paragraphs(df):
    corrected_paragraphs = []
    for paragraph in df['paragraph']:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=paragraph,
            max_tokens=250,
            n=1,
            stop=None,
            temperature=0.7
        )
        corrected_paragraph = response.choices[0].text.strip()
        corrected_paragraphs.append(corrected_paragraph)
    df['corrected_paragraph'] = corrected_paragraphs
    return df

def main():
    st.title("Corrección de errores gramaticales y de puntuación")
    st.write("Esta aplicación utiliza OpenAI Text Da Vinci 0.0.3 para corregir los errores gramaticales y de puntuación en el contenido de cada fila de un archivo CSV.")

    file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)
        st.write("Párrafos originales:")
        st.dataframe(df)

        df = correct_paragraphs(df)
        st.write("Párrafos corregidos:")
        st.dataframe(df)

        csv_file = df.to_csv(index=False)
        st.write("Descargar archivo CSV:")
        st.download_button("Descargar archivo CSV", data=csv_file, file_name="archivo_corregido.csv")

if __name__ == "__main__":
    main()
