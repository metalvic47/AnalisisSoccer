import streamlit as st
from utils import show_presentation
import streamlit as st
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
    
    # Resto de tu código aquí...
    
    # Miembros del equipo en columnas
    # st.subheader("Integrantes del Equipo")
    col1, col2, col3 = st.columns(3)

    with col1:
    # Centrar la imagen horizontalmente
        left2, center2, right2 = st.columns([1,1,1])
        with center2:
            st.image("image/edgar.webp", width=214)
        st.markdown("<h3 style='text-align: center;'>Edgar Hernández Rangel</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Rol:</strong> Analista de Datos</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Responsabilidades:</strong></p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>- Análisis exploratorio de datos</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>- Desarrollo de visualizaciones</p>", unsafe_allow_html=True)
        
    with col2:
        # Columnas anidadas para centrar la imagen
        left2, center2, right2 = st.columns([1,1,1])
        with center2:
            st.image("image/victor.webp", width=199)
        st.markdown("<h3 style='text-align: center;'>Victor Hugo Aguilar Cevallos</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Rol:</strong> Desarrollador</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Responsabilidades:</strong></p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>- Implementación de la aplicación</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>- Diseño de la interfaz</p>", unsafe_allow_html=True)
        
    with col3:
        # Columnas anidadas para centrar la imagen
        left3, center3, right3 = st.columns([1,1,1])
        with center3:
            st.image("image/victor.webp", width=199)
        st.markdown("<h3 style='text-align: center;'>Emiliano Hernández Rangel</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Rol:</strong> Científico de Datos</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Responsabilidades:</strong></p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>- Procesamiento de datos</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>- Análisis estadístico</p>", unsafe_allow_html=True)
    
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