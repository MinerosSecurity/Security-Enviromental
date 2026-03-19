import streamlit as st
import pandas as pd
import random
import datetime

# Configuración de la página web
st.set_page_config(page_title="Asignación de Charlas", page_icon="👷‍♂️")

st.title("Generador Aleatorio de Charlas 🎯")
st.write("Presiona el botón para elegir a una persona y un tema según el día de la semana.")

# Función para cargar los archivos CSV
@st.cache_data
def cargar_datos():
    personal = pd.read_csv('Personal.csv', header=None, names=['Nombre'])
    charlas = pd.read_csv('Charlas.csv')
    return personal, charlas

try:
    personal, charlas = cargar_datos()
    
    # Saber qué día es hoy
    dia_actual = datetime.datetime.now().weekday()
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    nombre_dia = dias_semana[dia_actual]

    # Regla: Martes (1) y Jueves (3) son Ambiente, los demás Seguridad
    if dia_actual == 1 or dia_actual == 3:
        categoria_del_dia = 'Medio Ambiente'
        color_texto = "#2e7d32" # Verde
    else:
        categoria_del_dia = 'Seguridad (SST)'
        color_texto = "#1565c0" # Azul

    st.markdown(f"### 📅 Hoy es **{nombre_dia}**")
    st.markdown(f"#### Categoría correspondiente: <span style='color:{color_texto};'>{categoria_del_dia}</span>", unsafe_allow_html=True)
    st.divider()

    # Botón gigante para generar
    if st.button("🎲 Seleccionar Persona y Tema Aleatorio", use_container_width=True):
        temas_filtrados = charlas[charlas['Categoría'] == categoria_del_dia]
        
        if temas_filtrados.empty:
            st.error(f"No hay temas disponibles para {categoria_del_dia}.")
        else:
            persona_elegida = random.choice(personal['Nombre'].tolist())
            tema_elegido = temas_filtrados.sample(n=1).iloc[0]

            # Mostrar los resultados en cuadros bonitos
            st.success("¡Sorteo realizado con éxito!")
            st.info(f"👤 **Expositor asignado:** {persona_elegida.strip()}")
            st.warning(f"📚 **Tema a exponer:** {tema_elegido['Tema de la Charla']}")
            
            # Si en tu archivo la columna se llama diferente (ej: Punto Clave), cámbialo aquí abajo:
            try:
                st.error(f"🎯 **Objetivo/Punto Clave:** {tema_elegido['Objetivo Principal']}")
            except:
                pass # Por si la columna de objetivo tiene otro nombre en tu archivo

except FileNotFoundError:
    st.error("⚠️ Faltan los archivos. Asegúrate de que 'Personal.csv' y 'Charlas.csv' estén junto a este archivo.")
