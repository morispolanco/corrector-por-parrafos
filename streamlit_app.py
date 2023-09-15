import streamlit as st
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
    st.title('Corrector gramatical y de puntuación')

    # Agregamos información de instrucciones
    st.write('Suba un archivo .CSV con las frases o textos que desea corregir.')

    # Pedimos al usuario que suba el archivo CSV
    archivo = st.file_uploader('Cargar archivo CSV', type=['csv'])

    if archivo:
        # Leemos el contenido del archivo y lo decodificamos como UTF-8
        contenido = archivo.read().decode('utf-8')

        # Creamos un objeto StringIO para leer el contenido como un archivo CSV
        archivo_csv = csv.reader(contenido.splitlines())

        # Convertimos el objeto CSV en una lista de filas
        filas = list(archivo_csv)

        # Creamos una lista para almacenar los resultados corregidos
        resultados = []

        # Iteramos sobre las filas del archivo CSV
        for fila in filas:
            # Obtenemos el texto de la fila
            texto = fila[0]

            # Corregimos el texto utilizando la API de OpenAI
            correccion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=texto,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.7,
                top_p=None,
                frequency_penalty=None,
                presence_penalty=None
            )

            # Obtenemos el texto corregido
            texto_corregido = correccion.choices[0].text

            # Agregamos el texto corregido a la lista de resultados
            resultados.append([texto, texto_corregido])

        # Guardamos los resultados en un archivo CSV
        with open("resultado.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(resultados)

        # Descargamos el archivo CSV
        with open("resultado.csv", "rb") as file:
            st.download_button("Descargar resultado", file)

E
