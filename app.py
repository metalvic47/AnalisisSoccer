import streamlit as st
from config import setup_page
import pandas as pd
from data_loader import load_data
from tabs import (
    team_presentation,
    historical_results,
    team_analysis,
    tournament_comparison,
    goal_patterns,
    continents_analysts,
    other_analysis,
)

# Configuración inicial
setup_page()
df = load_data()

df_countries = pd.read_csv('data/countries.csv', encoding='cp1252')  # Especificando la codificación correcta
df_shootouts = pd.read_csv('data/shootouts.csv')
df_goalscorers = pd.read_csv('data/goalscorers.csv')

# Crear una columna 'year' si no existe
if 'year' not in df.columns:
    df['year'] = pd.to_datetime(df['date']).dt.year

# Crear columna 'resultado' si no existe
if 'resultado' not in df.columns:
    df['resultado'] = df.apply(lambda row: 
        'Victoria Local' if row['home_score'] > row['away_score']
        else 'Victoria Visitante' if row['home_score'] < row['away_score']
        else 'Empate', axis=1)

# Título
st.title("⚽ Análisis Interactivo del Fútbol Internacional")

# Definición de tabs
tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👥 Presentación del Grupo",
    "📈 Resultados Históricos",
    "🔰 Análisis por Equipo",
    "🏆 Comparativa de Torneos",
    "⚽ Patrones de Goles",
    "🌎 Comparativa de Continentes",
    "💡 Otros Análisis"
])

# Contenido de cada tab
with tab0:
    team_presentation.show()
with tab1:
    historical_results.show(df)
with tab2:
    team_analysis.show(df)
with tab3:
    tournament_comparison.show(df)
with tab4:
    goal_patterns.show(df)
with tab5:
    continents_analysts.show(df, df_countries, df_shootouts)
with tab6:
    other_analysis.show(df, df_countries, df_goalscorers)