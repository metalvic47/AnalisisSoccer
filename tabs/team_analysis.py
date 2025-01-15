import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def show(df):
    st.header("🏆 Análisis por Equipo")
    
    # Selector de periodo en la parte superior
    años = df['year'].unique()
    start_year, end_year = st.select_slider(
        'Selecciona el período de análisis',
        options=años,
        value=(años.min(), años.max()),
        key="team_analysis_period"
    )
    
    # Filtrar datos por período
    df_filtered = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    
    # Obtener lista de equipos y asegurar que Ecuador esté como valor por defecto
    equipos = sorted(df_filtered['home_team'].unique())
    index_ecuador = equipos.index('Ecuador') if 'Ecuador' in equipos else 0
    
    # Selectores de equipo y tipo de análisis en una fila separada
    col1, col2 = st.columns(2)
    with col1:
        selected_team = st.selectbox(
            "Selecciona un equipo",
            equipos,
            index=index_ecuador  # Establecer Ecuador como valor por defecto
        )
    with col2:
        analysis_type = st.selectbox(
            "Tipo de análisis",
            ["Rendimiento General", "Goles", "Rivales Frecuentes"]
        )
    
    # Filtrar datos del equipo
    team_matches = df_filtered[
        (df_filtered['home_team'] == selected_team) | 
        (df_filtered['away_team'] == selected_team)
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
                title=f"Resultados como Local de {selected_team} ({start_year}-{end_year})"
            )
            st.plotly_chart(fig_home, use_container_width=True)
        
        with col_visitante:
            # Resultados como visitante
            away_matches = team_matches[team_matches['away_team'] == selected_team]
            away_results = away_matches['resultado'].value_counts()
            fig_away = px.pie(
                values=away_results.values,
                names=away_results.index,
                title=f"Resultados como Visitante de {selected_team} ({start_year}-{end_year})"
            )
            st.plotly_chart(fig_away, use_container_width=True)
        
        # Estadísticas adicionales
        st.markdown("### Estadísticas Detalladas")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            total_matches = len(team_matches)
            st.metric("Total de Partidos", total_matches)
        
        with stats_col2:
            win_rate = (team_matches['resultado'].str.contains('Victoria').sum() / total_matches * 100) if total_matches > 0 else 0
            st.metric("Porcentaje de Victorias", f"{win_rate:.1f}%")
        
        with stats_col3:
            avg_goals_home = team_matches[team_matches['home_team'] == selected_team]['home_score'].mean() or 0
            avg_goals_away = team_matches[team_matches['away_team'] == selected_team]['away_score'].mean() or 0
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
            title=f"Distribución de Goles de {selected_team} ({start_year}-{end_year})",
            yaxis_title="Goles por Partido",
            showlegend=True
        )
        
        st.plotly_chart(fig_goals, use_container_width=True)
        
    else:  # Rivales Frecuentes
        # Dividir en columnas para estadísticas y gráfico
        col_stats, col_graph = st.columns([1, 2])
        
        # Calcular estadísticas completas de rivalidades
        rival_stats = []
        for rival in df_filtered['home_team'].unique():
            if rival != selected_team:
                # Partidos como local
                local_matches = df_filtered[
                    (df_filtered['home_team'] == selected_team) & 
                    (df_filtered['away_team'] == rival)
                ]
                # Partidos como visitante
                away_matches = df_filtered[
                    (df_filtered['home_team'] == rival) & 
                    (df_filtered['away_team'] == selected_team)
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
        if not rivals_df.empty:
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
                    title=f"Top 10 Rivales más Frecuentes de {selected_team} ({start_year}-{end_year})",
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
        else:
            st.warning(f"No hay datos de rivales para {selected_team} en el período seleccionado.")