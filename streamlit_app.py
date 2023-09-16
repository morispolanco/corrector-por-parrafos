import streamlit as st
import pandas as pd
import openai
import csv

# Configuramos el diseño de la página
st.set_page_config(layout="wide")

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key

    # Agregamos un título al principio
    st.title('Corregir filas de un archivo CSV')

    # Agregamos información de instrucciones
    st.write('Suba un archivo CSV que desea corregir.')

    # Pedimos al usuario que suba el archivo CSV
    archivo = st.file_uploader('Cargar archivo CSV', type=['csv'])

    if archivo:
        # Leemos el contenido del archivo CSV
        df = pd.read_csv(archivo)

        # Creamos una lista para almacenar las filas corregidas
        filas_corregidas = []

        # Agregamos un botón para iniciar la corrección
        if st.button("Corregir"):
            # Iteramos sobre las filas del DataFrame
            for index, row in df.iterrows():
                # Obtenemos la fila como una lista de valores
                fila = row.tolist()

                # Convertimos la fila en una cadena separada por comas
                fila_str = ','.join(str(valor) for valor in fila)

                # Corregimos la fila utilizando la API de OpenAI
                correccion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=fila_str,
                    max_tokens=100,
                    n=1,
                    stop=None,
                    temperature=0.7,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )

                # Obtenemos la fila corregida
                fila_corregida = correccion.choices[0].text.strip()

                # Convertimos la fila corregida en una lista de valores
                fila_corregida_lista = fila_corregida.split(',')

                # Agregamos la fila corregida a la lista
                filas_corregidas.append(fila_corregida_lista)

            # Creamos un nuevo DataFrame con las filas corregidas
            df_corregido = pd.DataFrame(filas_corregidas)

            # Guardamos el DataFrame corregido en un archivo CSV
            df_corregido.to_csv("resultado.csv", index=False)

            # Generamos el enlace de descarga del archivo CSV
            with open("resultado.csv", "rb") as file:
                b64 = base64.b64encode(file.read()).decode()
                href = f'<a href="data:text/csv;base64,{b64}" download="resultado.csv">Descargar resultado CSV</a>'
                st.subheader("Archivo CSV generado:")
                st.markdown(href, unsafe_allow_html=True)
