# El código es muy largo para mostrarlo aquí - se divide en partes para mejor legibilidad.
# Ve la continuación en los siguientes mensajes.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Fútbol Internacional",
    page_icon="⚽",
    layout="wide"
)

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('./data/results.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['decade'] = (df['year'] // 10) * 10
    df['resultado'] = np.where(df['home_score'] > df['away_score'], 'Victoria Local',
                             np.where(df['home_score'] == df['away_score'], 'Empate', 
                                    'Victoria Visitante'))
    return df

df = load_data()

# Título y configuración
st.title("⚽ Análisis Interactivo del Fútbol Internacional")

# Tabs para diferentes visualizaciones
tab1, tab2, tab3, tab4 = st.tabs(["Resultados Históricos", "Análisis por Equipo", 
                                 "Comparativa de Torneos", "Patrones de Goles"])

# Tab 1: Resultados Históricos
with tab1:
    st.header("📈 Evolución Histórica de Resultados")
    
    # Selector de periodo
    años = df['year'].unique()
    start_year, end_year = st.select_slider(
        'Selecciona el período de análisis',
        options=años,
        value=(años.min(), años.max())
    )
    
    # Filtrar datos por período
    mask = (df['year'] >= start_year) & (df['year'] <= end_year)
    df_filtered = df[mask]
    
    # Gráfico interactivo de evolución
    fig_evolution = go.Figure()
    
    for resultado in ['Victoria Local', 'Empate', 'Victoria Visitante']:
        yearly_stats = df_filtered[df_filtered['resultado'] == resultado].groupby('year').size()
        fig_evolution.add_trace(
            go.Scatter(
                x=yearly_stats.index,
                y=yearly_stats.values,
                name=resultado,
                mode='lines+markers',
                hovertemplate="Año: %{x}<br>" +
                             "Cantidad: %{y}<br>" +
                             "<extra></extra>"
            )
        )
    
    fig_evolution.update_layout(
        title="Evolución de Resultados a lo Largo del Tiempo",
        xaxis_title="Año",
        yaxis_title="Cantidad de Partidos",
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Gráfico de proporción
    yearly_proportions = df_filtered.pivot_table(
        index='year',
        columns='resultado',
        aggfunc='size',
        fill_value=0
    ).apply(lambda x: x/x.sum()*100, axis=1)
    
    fig_prop = px.area(
        yearly_proportions,
        labels={'value': 'Porcentaje', 'year': 'Año'},
        title='Proporción de Resultados por Año'
    )
    
    st.plotly_chart(fig_prop, use_container_width=True)

    # Tab 2: Análisis por Equipo
with tab2:
    st.header("🏆 Análisis por Equipo")
    
    # Selectores de equipo y tipo de análisis
    col1, col2 = st.columns(2)
    with col1:
        selected_team = st.selectbox(
            "Selecciona un equipo",
            sorted(df['home_team'].unique())
        )
    with col2:
        analysis_type = st.selectbox(
            "Tipo de análisis",
            ["Rendimiento General", "Goles", "Rivales Frecuentes"]
        )
    
    # Filtrar datos del equipo
    team_matches = df[
        (df['home_team'] == selected_team) | 
        (df['away_team'] == selected_team)
    ]
    
    if analysis_type == "Rendimiento General":
        # Crear dos columnas para los gráficos
        col_local, col_visitante = st.columns(2)
        
        with col_local:
            # Resultados como local
            home_results = team_matches[team_matches['home_team'] == selected_team]['resultado'].value_counts()
            fig_home = px.pie(
                values=home_results.values,
                names=home_results.index,
                title=f"Resultados como Local de {selected_team}"
            )
            st.plotly_chart(fig_home, use_container_width=True)
        
        with col_visitante:
            # Resultados como visitante
            away_matches = team_matches[team_matches['away_team'] == selected_team]
            away_results = away_matches['resultado'].value_counts()
            fig_away = px.pie(
                values=away_results.values,
                names=away_results.index,
                title=f"Resultados como Visitante de {selected_team}"
            )
            st.plotly_chart(fig_away, use_container_width=True)
        
        # Estadísticas adicionales
        st.markdown("### Estadísticas Detalladas")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            total_matches = len(team_matches)
            st.metric("Total de Partidos", total_matches)
        
        with stats_col2:
            win_rate = (team_matches['resultado'].str.contains('Victoria').sum() / total_matches * 100)
            st.metric("Porcentaje de Victorias", f"{win_rate:.1f}%")
        
        with stats_col3:
            avg_goals_home = team_matches[team_matches['home_team'] == selected_team]['home_score'].mean()
            avg_goals_away = team_matches[team_matches['away_team'] == selected_team]['away_score'].mean()
            avg_goals = (avg_goals_home + avg_goals_away) / 2
            st.metric("Promedio de Goles por Partido", f"{avg_goals:.2f}")
    
    elif analysis_type == "Goles":
        # Gráfico de goles
        fig_goals = go.Figure()
        
        # Goles como local
        home_goals = team_matches[team_matches['home_team'] == selected_team]['home_score']
        away_goals = team_matches[team_matches['away_team'] == selected_team]['away_score']
        
        fig_goals.add_trace(
            go.Box(
                y=home_goals,
                name="Goles como Local",
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            )
        )
        
        fig_goals.add_trace(
            go.Box(
                y=away_goals,
                name="Goles como Visitante",
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            )
        )
        
        fig_goals.update_layout(
            title=f"Distribución de Goles de {selected_team}",
            yaxis_title="Goles por Partido",
            showlegend=True
        )
        
        st.plotly_chart(fig_goals, use_container_width=True)
        
    else:  # Rivales Frecuentes
        # Dividir en columnas para estadísticas y gráfico
        col_stats, col_graph = st.columns([1, 2])
        
        # Calcular estadísticas completas de rivalidades
        rival_stats = []
        for rival in df['home_team'].unique():
            if rival != selected_team:
                # Partidos como local
                local_matches = df[
                    (df['home_team'] == selected_team) & 
                    (df['away_team'] == rival)
                ]
                # Partidos como visitante
                away_matches = df[
                    (df['home_team'] == rival) & 
                    (df['away_team'] == selected_team)
                ]
                
                total_matches = len(local_matches) + len(away_matches)
                if total_matches > 0:
                    # Victorias como local
                    wins_local = len(local_matches[local_matches['home_score'] > local_matches['away_score']])
                    # Victorias como visitante
                    wins_away = len(away_matches[away_matches['away_score'] > away_matches['home_score']])
                    # Total victorias
                    total_wins = wins_local + wins_away
                    
                    rival_stats.append({
                        'rival': rival,
                        'total_matches': total_matches,
                        'victories': total_wins,
                        'win_rate': (total_wins / total_matches) * 100,
                        'goals_favor': (
                            local_matches['home_score'].sum() + 
                            away_matches['away_score'].sum()
                        ),
                        'goals_against': (
                            local_matches['away_score'].sum() + 
                            away_matches['home_score'].sum()
                        )
                    })
        
        # Convertir a DataFrame y ordenar
        rivals_df = pd.DataFrame(rival_stats)
        rivals_df = rivals_df.sort_values('total_matches', ascending=False).head(10)
        
        # Gráfico de barras mejorado
        with col_graph:
            fig_rivals = go.Figure()
            
            # Barra principal para total de partidos
            fig_rivals.add_trace(
                go.Bar(
                    name='Total Partidos',
                    y=rivals_df['rival'],
                    x=rivals_df['total_matches'],
                    orientation='h',
                    marker_color='lightgray',
                    text=rivals_df['total_matches'],
                    textposition='auto',
                )
            )
            
            # Barra superpuesta para victorias
            fig_rivals.add_trace(
                go.Bar(
                    name='Victorias',
                    y=rivals_df['rival'],
                    x=rivals_df['victories'],
                    orientation='h',
                    marker_color='green',
                    text=rivals_df['victories'],
                    textposition='inside',
                )
            )
            
            fig_rivals.update_layout(
                title=f"Top 10 Rivales más Frecuentes de {selected_team}",
                xaxis_title="Número de Partidos",
                yaxis_title="Rival",
                barmode='overlay',
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig_rivals, use_container_width=True)
        
        # Tabla de estadísticas
        with col_stats:
            st.markdown("### Estadísticas Detalladas")
            
            # Formatear datos para la tabla
            rivals_df['win_rate'] = rivals_df['win_rate'].round(1)
            rivals_df['avg_goals_favor'] = (rivals_df['goals_favor'] / rivals_df['total_matches']).round(2)
            rivals_df['avg_goals_against'] = (rivals_df['goals_against'] / rivals_df['total_matches']).round(2)
            
            # Mostrar tabla con estadísticas clave
            st.dataframe(
                rivals_df[['rival', 'total_matches', 'victories', 'win_rate', 
                          'avg_goals_favor', 'avg_goals_against']]
                .rename(columns={
                    'rival': 'Rival',
                    'total_matches': 'Partidos',
                    'victories': 'Victorias',
                    'win_rate': '% Victoria',
                    'avg_goals_favor': 'Goles a Favor (Prom)',
                    'avg_goals_against': 'Goles en Contra (Prom)'
                })
            )
# Tab 3: Comparativa de Torneos
with tab3:
    st.header("🏆 Comparativa de Torneos")
    
    # Selector de torneos
    selected_tournaments = st.multiselect(
        "Selecciona torneos para comparar",
        df['tournament'].unique(),
        default=['FIFA World Cup', 'UEFA Euro', 'Copa América']
    )
    
    if selected_tournaments:
        tournament_data = df[df['tournament'].isin(selected_tournaments)]
        
        # Crear gráfico de resultados por torneo
        fig_tournaments = go.Figure()
        
        for torneo in selected_tournaments:
            torneo_stats = tournament_data[tournament_data['tournament'] == torneo]['resultado'].value_counts(normalize=True) * 100
            
            fig_tournaments.add_trace(
                go.Bar(
                    name=torneo,
                    x=['Victoria Local', 'Empate', 'Victoria Visitante'],
                    y=torneo_stats.reindex(['Victoria Local', 'Empate', 'Victoria Visitante']).values,
                    text=torneo_stats.round(1).values.astype(str) + '%',
                    textposition='auto',
                )
            )
        
        fig_tournaments.update_layout(
            title="Comparativa de Resultados por Torneo",
            xaxis_title="Resultado",
            yaxis_title="Porcentaje",
            barmode='group'
        )
        
        st.plotly_chart(fig_tournaments, use_container_width=True)

# Tab 4: Patrones de Goles
with tab4:
    # Dentro del tab4 (Patrones de Goles), modificamos la parte del heatmap
    st.header("⚽ Patrones de Goles")

    # Explicación del heatmap
    st.markdown("""
        ### Frecuencia de Resultados
        El siguiente mapa de calor muestra qué tan común es cada resultado. Por ejemplo:
        - El eje Y (vertical) muestra los goles del equipo **local**
        - El eje X (horizontal) muestra los goles del equipo **visitante**
        - Los colores más intensos indican resultados más frecuentes
        - Cada celda muestra el número de veces que ocurrió ese resultado
    """)

    # Crear heatmap de goles mejorado
    goles_matrix = pd.crosstab(df['home_score'], df['away_score'])

    # Limitamos a resultados más comunes (0-7 goles) para mejor visualización
    goles_matrix = goles_matrix.loc[0:7, 0:7]

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=goles_matrix.values,
            x=goles_matrix.columns,
            y=goles_matrix.index,
            colorscale='RdYlBu_r',
            text=goles_matrix.values,
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False,
            hovertemplate="Local: %{y} goles<br>Visitante: %{x} goles<br>Frecuencia: %{text}<extra></extra>"
        )
    )

    fig_heatmap.update_layout(
        title={
            'text': "Frecuencia de Resultados (número de partidos con cada marcador)",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Goles del Equipo Visitante",
        yaxis_title="Goles del Equipo Local",
        width=800,
        height=600
    )

    # Añadir ejemplos de cómo interpretar
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Ejemplos de interpretación
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Ejemplos de interpretación:")
        resultado_ejemplo = goles_matrix.loc[1,0]
        st.write(f"• El resultado 1-0 (victoria local) ocurrió {resultado_ejemplo} veces")
        resultado_ejemplo_2 = goles_matrix.loc[2,1]
        st.write(f"• El resultado 2-1 (victoria local) ocurrió {resultado_ejemplo_2} veces")

    with col2:
        # Encontrar el resultado más común
        max_val = goles_matrix.max().max()
        max_idx = np.where(goles_matrix == max_val)
        max_home = max_idx[0][0]
        max_away = max_idx[1][0]
        st.markdown("#### Resultado más común:")
        st.write(f"• El marcador {max_home}-{max_away} es el más frecuente con {max_val} partidos")
    
    # Estadísticas adicionales
    st.markdown("### Estadísticas de Goles")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        max_goles = df['home_score'].max()
        st.metric("Máximo de Goles en un Partido (Local)", max_goles)
        partido_max_goles = df[df['home_score'] == max_goles].iloc[0]
        st.write(f"{partido_max_goles['home_team']} {int(partido_max_goles['home_score'])} - "
                 f"{int(partido_max_goles['away_score'])} {partido_max_goles['away_team']}")
    
    with col4:
        promedio_goles = (df['home_score'] + df['away_score']).mean()
        st.metric("Promedio de Goles por Partido", f"{promedio_goles:.2f}")
    
    with col5:
        partidos_sin_goles = len(df[(df['home_score'] == 0) & (df['away_score'] == 0)])
        porcentaje_sin_goles = (partidos_sin_goles / len(df)) * 100
        st.metric("Partidos Sin Goles", f"{partidos_sin_goles} ({porcentaje_sin_goles:.1f}%)")

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

# Footer con información adicional
st.markdown("""
---
### 📈 Notas del Análisis:
- Los datos incluyen partidos internacionales desde 1872 hasta 2024
- Se consideran todos los torneos internacionales y amistosos
- Las estadísticas se actualizan en tiempo real según los filtros seleccionados
""")