import streamlit as st

def show_general_metrics(df):
    # Métricas generales
    st.markdown("### 📊 Métricas Generales")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_matches = len(df)
        st.metric("Total de Partidos", f"{total_matches:,}")

    with col2:
        avg_goals = (df['home_score'] + df['away_score']).mean()
        st.metric("Promedio de Goles por Partido", f"{avg_goals:.2f}")

    with col3:
        home_wins = (df['resultado'] == 'Victoria Local').mean() * 100
        st.metric("% Victorias Locales", f"{home_wins:.1f}%")

    with col4:
        most_common_score = f"{df['home_score'].mode().iloc[0]}-{df['away_score'].mode().iloc[0]}"
        st.metric("Resultado más Común", most_common_score)


def show_presentation():
    # Footer con información adicional
    st.markdown("""
    ---
    ### 📈 Notas del Análisis:
    - Los datos incluyen partidos internacionales desde 1872 hasta 2024.
    - Se consideran todos los torneos internacionales y amistosos, excepto juegos olímpicos, los partidos son únicamente de selecciones de hombres.
    - Las estadísticas se actualizan en tiempo real según los filtros seleccionados.
    - La fuente de datos es kaggle.com que a su vez obtuvo de Wikipedia, rsssf.com y sitios web individuales de asociaciones de fútbol.
     ### 🔥 Desarrollo:
    Python, Streamlit, Github, Visual Studio Code
     ### ℹ️ Disclaimer:
    Esta es una versión preliminar
    ### 🫶🏻 Agradecimiento:
    Profe Andre, profe Cris, señor X, K-malogan, generación III de Análisis de Datos y Kruger IE
    """)