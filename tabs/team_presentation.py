import streamlit as st
from utils import show_presentation

def show():
    # SVG como código HTML con escape de comillas
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
    
    # Mostrar el SVG usando st.markdown
    st.markdown(svg_content, unsafe_allow_html=True)
    
    # Eslogan centrado
    st.markdown("<h2 style='text-align: center; color: #2E86C1; margin-bottom: 30px;'>Analizamos tus datos para que tomes la mejor decisión y ganes más dinero!</h2>", unsafe_allow_html=True)
    
    # Miembros del equipo en cuadrícula 2x2
    st.subheader("Integrantes del Equipo")
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # Primera fila, primera columna
    with row1_col1:
        left, center, right = st.columns([1,1,1])
        with center:
            st.image("image/edgar.webp", width=214)
        st.markdown("<h3 style='text-align: center;'>Edgar Molina</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>(<strong>Edgar King 👑</strong>)</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Arquitecto de patrones de datos</strong></p>", unsafe_allow_html=True)

    # Primera fila, segunda columna
    with row1_col2:
        left, center, right = st.columns([1,1,1])
        with center:
            st.image("image/victor.webp", width=199)
        st.markdown("<h3 style='text-align: center;'>Victor Aguilar</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>(<strong>Victor King 👑</strong>)</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Especialista en Visualización</strong></p>", unsafe_allow_html=True) 
    
    # Segunda fila, primera columna
    with row2_col1:
        left, center, right = st.columns([1,1,1])
        with center:
            st.image("image/emiliano.webp", width=220)
        st.markdown("<h3 style='text-align: center;'>Emiliano Ehlers</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>(<strong>Emiliano King 👑</strong>)</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Maestro de analisis de datos</strong></p>", unsafe_allow_html=True)


    # Segunda fila, segunda columna
    with row2_col2:
        left, center, right = st.columns([1,1,1])
        with center:
            st.image("image/marcos.webp", width=199)
        st.markdown("<h3 style='text-align: center;'>Marcos Plata</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 20px;'>(<strong>Marcos king 👑</strong>)</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>El genio</strong></p>", unsafe_allow_html=True)

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

    show_presentation()