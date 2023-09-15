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
        # Leemos el archivo CSV en modo de texto
        reader = csv.reader(archivo.decode('utf-8').splitlines())
        filas = list(reader)

        # Resto del código...




    # Agregamos un botón para iniciar la corrección
    if st.button('Corregir'):
        # Utilizamos la API de GPT-3 para corregir cada fila
        resultados = []
        for i, fila in enumerate(filas):
            texto = fila[0]  # Suponemos que el texto se encuentra en la primera columna

            # Utilizamos la API de OpenAI para corregir la gramática y la puntuación
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=texto,
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None,
                timeout=5
            )
            correccion = response.choices[0].text.strip()

            # Agregamos la corrección a la lista de resultados
            resultados.append(correccion)

        # Guardamos los resultados en un archivo CSV
        with open('correcciones.csv', 'w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(['Texto corregido'])
            writer.writerows(resultados)

        # Mostramos un botón para descargar el archivo CSV
        st.download_button('Descargar correcciones', 'correcciones.csv', 'Click aquí para descargar el archivo CSV')
