import streamlit as st
from utils import show_presentation
import os
import base64
def show():
    # Contenido SVG como HTML
    svg_content = """
    <div style='display: flex; justify-content: center; margin: 20px 0;'>
        <div style='width: 400px;'>
            <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 500'>
                <defs>
                    <linearGradient id='mainGradient' x1='0%' y1='0%' x2='100%' y2='100%'>
                        <stop offset='0%' style='stop-color:#2E86C1'/>
                        <stop offset='100%' style='stop-color:#17A589'/>
                    </linearGradient>
                    <linearGradient id='barGradient' x1='0%' y1='0%' x2='0%' y2='100%'>
                        <stop offset='0%' style='stop-color:#3498DB'/>
                        <stop offset='100%' style='stop-color:#2874A6'/>
                    </linearGradient>
                </defs>
                <g transform='translate(0, -30)'>
                    <circle cx='250' cy='250' r='180' fill='none' stroke='url(#mainGradient)' stroke-width='15'/>
                    <g transform='translate(250,250) rotate(-30)'>
                        <rect x='-100' y='-120' width='20' height='80' fill='url(#barGradient)' rx='5'/>
                        <rect x='-60' y='-140' width='20' height='100' fill='url(#barGradient)' rx='5'/>
                        <rect x='-20' y='-160' width='20' height='120' fill='url(#barGradient)' rx='5'/>
                        <rect x='20' y='-140' width='20' height='100' fill='url(#barGradient)' rx='5'/>
                        <rect x='60' y='-120' width='20' height='80' fill='url(#barGradient)' rx='5'/>
                    </g>
                    <path d='M150 280 Q250 180 350 280' fill='none' stroke='#3498DB' stroke-width='8' stroke-linecap='round'/>
                    <circle cx='150' cy='280' r='8' fill='#2E86C1'/>
                    <circle cx='250' cy='180' r='8' fill='#2E86C1'/>
                    <circle cx='350' cy='280' r='8' fill='#2E86C1'/>
                    <path d='M160 320 Q250 290 340 320 L340 350 Q250 380 160 350 Z' fill='url(#mainGradient)'/>
                </g>
                <text x='250' y='470' text-anchor='middle' font-family='Arial Black, sans-serif' font-size='45' font-weight='bold' fill='#2E86C1' letter-spacing='2'>
                    DATA KINGS
                </text>
            </svg>
        </div>
    </div>
    """

    # Mostrar el SVG
    st.markdown(svg_content, unsafe_allow_html=True)

    # Eslogan centrado
    st.markdown(
        "<h2 style='text-align: center; color: #2E86C1; margin-bottom: 30px;'>"
        "Analizamos tus datos para que tomes la mejor decisión y ganes más dinero!"
        "</h2>",
        unsafe_allow_html=True
    )
    
    # st.subheader("Integrantes del Equipo")
    
    # Información del equipo
    team_members = [
        {
            "name": "Edgar Molina",
            "title": "Arquitecto de patrones de datos",
            "role": "Edgar King 👑",
            "image": "image/edgar.webp"
        },
        {
            "name": "Victor Aguilar",
            "title": "Especialista en Visualización",
            "role": "Victor King 👑",
            "image": "image/victor.webp"
        },
        {
            "name": "Emiliano Ehlers",
            "title": "Maestro de análisis de datos",
            "role": "Emiliano King 👑",
            "image": "image/emiliano.webp"
        },
        {
            "name": "Marcos Plata",
            "title": "El genio",
            "role": "Marcos King 👑",
            "image": "image/marcos.webp"
        },
    ]


    # Mostramos los integrantes en parejas de columnas (2 por fila)
    for i in range(0, len(team_members), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            index = i + j
            if index < len(team_members):
                member = team_members[index]

                # 1. Convertimos la imagen en Base64
                if os.path.exists(member["image"]):
                    with open(member["image"], "rb") as f:
                        img_bytes = f.read()
                    encoded_img = base64.b64encode(img_bytes).decode("utf-8")
                else:
                    encoded_img = ""

                # 2. HTML sin indentación, con flexbox, todo en un solo bloque
                html_code = f"""<div style="display: flex; flex-direction: column; 
                                     align-items: center; justify-content: center; 
                                     text-align: center; padding: 10px 0;">
    <img 
        src="data:image/webp;base64,{encoded_img}" 
        alt="{member['name']}"
        style="width:150px; border-radius:10px; margin-bottom:10px;"
    />
    <p style="margin: 0; font-weight: bold; font-size: 1.1rem;">
        {member['name']}
    </p>
    <p style="margin: 5px 0; font-style: italic;">
        {member['role']}
    </p>
    <p style="margin: 5px 0; color: gray;">
        {member['title']}
    </p>
</div>"""

                # 3. Renderizamos el bloque HTML
                col.markdown(html_code, unsafe_allow_html=True)

    # Sección de objetivos
    st.subheader("🎯 Objetivos del Proyecto")
    with st.expander("Ver Objetivos"):
        st.write("""
        1. **Objetivo Principal**  
           - Analizar patrones históricos en resultados de fútbol internacional

        2. **Objetivos Específicos**  
           - Identificar tendencias en resultados de partidos  
           - Analizar el rendimiento de equipos específicos  
           - Visualizar patrones de goles y resultados  
           - Comparar diferentes torneos internacionales
        """)
    
    # Sección de metodología
    st.subheader("📊 Metodología")
    with st.expander("Ver Metodología"):
        st.write("""
        Nuestro enfoque incluyó las siguientes etapas:
        1. Recolección y limpieza de datos
        2. Análisis exploratorio
        3. Desarrollo de visualizaciones
        4. Implementación de la aplicación interactiva
        """)

    # Llamada a la función show_presentation() (si existe en tu utils.py)
    show_presentation()
