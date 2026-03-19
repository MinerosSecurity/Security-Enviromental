import pandas as pd
import random
import datetime
import ipywidgets as widgets
from IPython.display import clear_output, display, HTML

def realizar_sorteo(b):
    clear_output()
    display(boton_sorteo) # Volver a mostrar el botón

    try:
        # Cargar los archivos
        # Specify 'latin1' encoding for files that might contain non-UTF-8 characters like 'ñ'
        personal = pd.read_csv('Personal.csv', header=None, names=['Nombre'], encoding='latin1')
        charlas = pd.read_csv('Charlas.csv', encoding='latin1')

        # Determinar el día y la categoría
        dia_actual = datetime.datetime.now().weekday()
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        nombre_dia = dias_semana[dia_actual]

        if dia_actual == 1 or dia_actual == 3: # Martes y Jueves
            categoria_del_dia = 'Medio Ambiente'
            color = "#2e7d32" # Verde
        else:
            categoria_del_dia = 'Seguridad (SST)'
            color = "#1565c0" # Azul

        temas_filtrados = charlas[charlas['Categoría'] == categoria_del_dia]

        # Mostrar cabecera
        display(HTML(f"<h2>📅 Hoy es {nombre_dia}</h2>"))
        display(HTML(f"<h3>Categoría: <span style='color:{color};'>{categoria_del_dia}</span></h3><hr>"))

        if temas_filtrados.empty:
            display(HTML("<p style='color:red;'>No hay temas disponibles para esta categoría.</p>"))
            return

        # Sorteo
        persona_elegida = random.choice(personal['Nombre'].tolist())
        tema_elegido = temas_filtrados.sample(n=1).iloc[0]

        # Resultados
        display(HTML(f"<h4>👤 <b>Expositor asignado:</b> {persona_elegida.strip()}</h4>"))
        display(HTML(f"<h4>📚 <b>Tema de la Charla:</b> {tema_elegido['Tema de la Charla']}</h4>"))

        try:
            display(HTML(f"<h4>🎯 <b>Objetivo Principal:</b> {tema_elegido['Objetivo Principal']}</h4>"))
        except:
            pass # Por si la columna se llama diferente

    except FileNotFoundError:
        display(HTML("<h4 style='color:red;'>⚠️ Error: No encuentro los archivos. Asegúrate de subir 'Personal.csv' y 'Charlas.csv' en la carpeta de la izquierda.</h4>"))

# Crear el botón interactivo
boton_sorteo = widgets.Button(
    description='🎲 Sortear Charla',
    disabled=False,
    button_style='success',
    tooltip='Haz clic para elegir persona y tema',
    icon='check'
)

# Qué hacer cuando se hace clic
boton_sorteo.on_click(realizar_sorteo)

# Mostrar el botón por primera vez
display(boton_sorteo)
