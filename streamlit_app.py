import streamlit as st
import docx2txt
import docx
import openai

# Configuramos el diseño de la página
st.set_page_config(layout="wide")

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key

    # Agregamos un título al principio
    st.title('Corrector gramatical y de puntuación')

    # Agregamos información de instrucciones
    st.write('Suba un archivo de documento (.docx) que desea corregir.')

    # Pedimos al usuario que suba el archivo de documento
    archivo = st.file_uploader('Cargar archivo de documento', type=['docx'])

    if archivo:
        # Leemos el contenido del archivo de documento
        contenido = docx2txt.process(archivo)

        # Creamos un objeto Document para almacenar el contenido corregido
        doc_corregido = docx.Document()

        # Dividimos el contenido en párrafos
        parrafos = contenido.split('\n')

        # Iteramos sobre los párrafos
        for parrafo in parrafos:
            # Corregimos el párrafo utilizando la API de OpenAI
            correccion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=parrafo,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
                top_p=None,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Obtenemos el párrafo corregido
            parrafo_corregido = correccion.choices[0].text

            # Agregamos el párrafo corregido al documento
            doc_corregido.add_paragraph(parrafo_corregido)

        # Guardamos el documento corregido en un archivo .docx
        doc_corregido.save("resultado.docx")

        # Descargamos el archivo .docx
        with open("resultado.docx", "rb") as file:
            st.download_button("Descargar resultado", file, file_name="resultado.docx")

