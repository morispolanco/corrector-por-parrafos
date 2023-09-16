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

        # Dividimos el contenido en párrafos
        parrafos = contenido.split('\n')

        # Creamos una lista para almacenar los párrafos corregidos
        parrafos_corregidos = []

        # Agregamos un botón para iniciar la corrección
        if st.button("Corregir"):
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
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )

                # Obtenemos el párrafo corregido
                parrafo_corregido = correccion.choices[0].text.strip()

                # Agregamos el párrafo corregido a la lista
                parrafos_corregidos.append(parrafo_corregido)

            # Creamos un archivo CSV para almacenar los párrafos corregidos
            with open("resultado.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Párrafo corregido"])
                writer.writerows(zip(parrafos_corregidos))

            # Mostramos el enlace para descargar el archivo CSV
            st.subheader("Archivo CSV generado:")
            st.markdown("[Descargar resultado CSV](resultado.csv)")

            # Creamos un nuevo archivo DOC con los párrafos corregidos
            doc_corregido = docx.Document()
            for parrafo_corregido in parrafos_corregidos:
                doc_corregido.add_paragraph(parrafo_corregido)

            # Guardamos el documento corregido en un archivo .docx
            doc_corregido.save("resultado.docx")

            # Mostramos el enlace para descargar el archivo DOC
            st.subheader("Archivo DOC generado:")
            st.markdown("[Descargar resultado DOC](resultado.docx)")
