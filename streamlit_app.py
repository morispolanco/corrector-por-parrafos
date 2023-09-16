import streamlit as st
import docx2txt
import docx
import csv
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
    st.title('Convertir DOC a CSV y corregir gramática y estilo')

    # Agregamos información de instrucciones
    st.write('Suba un archivo de documento (.docx) que desea convertir a CSV y corregir.')

    # Pedimos al usuario que suba el archivo de documento
    archivo = st.file_uploader('Cargar archivo de documento', type=['docx'])

    if archivo:
        # Leemos el contenido del archivo de documento
        contenido = docx2txt.process(archivo)

        # Dividimos el contenido en chunks delimitados por el carácter de párrafo
        chunks = contenido.split('\n\n')

        # Creamos una lista para almacenar los chunks corregidos
        chunks_corregidos = []

        # Agregamos un botón para iniciar la corrección
        if st.button("Corregir"):
            # Iteramos sobre los chunks
            for chunk in chunks:
                # Corregimos el chunk utilizando la API de OpenAI
                correccion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=chunk,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.7,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )

                # Obtenemos el chunk corregido
                chunk_corregido = correccion.choices[0].text.strip()

                # Agregamos el chunk corregido a la lista
                chunks_corregidos.append(chunk_corregido)

            # Creamos un nuevo archivo DOCX con los chunks corregidos
            doc_corregido = docx.Document()
            for chunk_corregido in chunks_corregidos:
                doc_corregido.add_paragraph(chunk_corregido)

            # Guardamos el documento corregido en un archivo .docx
            doc_corregido.save("resultado.docx")

            # Mostramos el enlace para descargar el archivo DOCX
            st.subheader("Archivo DOCX generado:")
            st.markdown(get_binary_file_downloader_html("resultado.docx", "Descargar resultado DOCX"), unsafe_allow_html=True)
