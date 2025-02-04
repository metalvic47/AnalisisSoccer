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
            local_matches = team_matches[team_matches['home_team'] == selected_team]
            local_results = pd.Series({
                'Victoria': sum(local_matches['home_score'] > local_matches['away_score']),
                'Empate': sum(local_matches['home_score'] == local_matches['away_score']),
                'Derrota': sum(local_matches['home_score'] < local_matches['away_score'])
            })
            
            fig_home = px.pie(
                values=local_results.values,
                names=local_results.index,
                title=f"Resultados como Local de {selected_team} ({start_year}-{end_year})",
                color_discrete_sequence=["#2085ec" , "#cea9bc ", "#72b4eb"]
                
            )
            st.plotly_chart(fig_home, use_container_width=True)
        
        with col_visitante:
            # Resultados como visitante
            away_matches = team_matches[team_matches['away_team'] == selected_team]
            away_results = pd.Series({
                'Victoria': sum(away_matches['away_score'] > away_matches['home_score']),
                'Empate': sum(away_matches['away_score'] == away_matches['home_score']),
                'Derrota': sum(away_matches['away_score'] < away_matches['home_score'])
            })
            
            fig_away = px.pie(
                labels=['Victoria', 'Empate', 'Derrota'],
                values=away_results.values,
                names=away_results.index,
                title=f"Resultados como Visitante de {selected_team} ({start_year}-{end_year})",
                color_discrete_sequence=["#cea9bc", "#72b4eb ", "#2085ec"]
                
            )
            st.plotly_chart(fig_away, use_container_width=True)
        
        # Estadísticas adicionales
        st.markdown("### Estadísticas Detalladas")
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            total_matches = len(team_matches)
            st.metric("Total de Partidos", total_matches)
        
        with stats_col2:
            # Calcular victorias totales (local + visitante)
            victorias_local = sum((team_matches['home_team'] == selected_team) & 
                                (team_matches['home_score'] > team_matches['away_score']))
            victorias_visitante = sum((team_matches['away_team'] == selected_team) & 
                                    (team_matches['away_score'] > team_matches['home_score']))
            total_wins = victorias_local + victorias_visitante
            win_rate = (total_wins / total_matches * 100) if total_matches > 0 else 0
            st.metric("Porcentaje de Victorias", f"{win_rate:.1f}%")
        
        with stats_col3:
            # Calcular promedio de goles a favor
            goles_favor = (
                team_matches[team_matches['home_team'] == selected_team]['home_score'].sum() +
                team_matches[team_matches['away_team'] == selected_team]['away_score'].sum()
            )
            avg_goals = goles_favor / total_matches if total_matches > 0 else 0
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
        #st.markdown("Ya pana")
        st.markdown(f"### Estadísticas Detalladas")
        col_stats, col_graph = st.columns([1, 1])
        
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
                    xaxis_title="Número de Partidos",
                    yaxis_title="Rival",
                    barmode='overlay',
                    showlegend=True,
                    height=500                    
                )
                
                st.plotly_chart(fig_rivals, use_container_width=True)
            
            # Tabla de estadísticas
            with col_stats:
                st.markdown(f"### Top 10 Rivales más Frecuentes de {selected_team} ({start_year} - {end_year})")
                        
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
                        'avg_goals_favor': 'GF (Prom)',
                        'avg_goals_against': 'GC (Prom)'
                    })
                )
        else:
            st.warning(f"No hay datos de rivales para {selected_team} en el período seleccionado.")
        # Después del último else y su código...
    
    # Análisis General de Equipos
    st.markdown("---")
    st.subheader("📊 Análisis General de Equipos")
    
    # Crear métricas para todos los equipos
    equipos_stats = []
    for equipo in equipos:
        matches = df_filtered[
            (df_filtered['home_team'] == equipo) | 
            (df_filtered['away_team'] == equipo)
        ]
        
        if len(matches) > 0:
            # Victorias como local
            victorias_local = sum((matches['home_team'] == equipo) & 
                                (matches['home_score'] > matches['away_score']))
            # Victorias como visitante
            victorias_visitante = sum((matches['away_team'] == equipo) & 
                                    (matches['away_score'] > matches['home_score']))
            
            # Total victorias
            total_victorias = victorias_local + victorias_visitante
            
            # Goles a favor
            goles_favor = (
                matches[matches['home_team'] == equipo]['home_score'].sum() +
                matches[matches['away_team'] == equipo]['away_score'].sum()
            )
            
            equipos_stats.append({
                'equipo': equipo,
                'partidos': len(matches),
                'victorias': total_victorias,
                'goles': goles_favor
            })
    
    if equipos_stats:
        df_stats = pd.DataFrame(equipos_stats)
        
        # Crear tres columnas para las métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Equipo con más partidos
            max_partidos = df_stats.loc[df_stats['partidos'].idxmax()]
            st.metric(
                "Equipo con Más Partidos",
                max_partidos['equipo'],
                f"{max_partidos['partidos']} partidos"
            )
        
        with col2:
            # Equipo con más victorias
            max_victorias = df_stats.loc[df_stats['victorias'].idxmax()]
            st.metric(
                "Equipo con Más Victorias",
                max_victorias['equipo'],
                f"{int(max_victorias['victorias'])} victorias"
            )
        
        with col3:
            # Equipo con más goles
            max_goles = df_stats.loc[df_stats['goles'].idxmax()]
            st.metric(
                "Equipo Más Goleador",
                max_goles['equipo'],
                f"{int(max_goles['goles'])} goles"
            )
        
        # Gráfico comparativo de los mejores equipos
        fig_top = go.Figure()
        
        # Top 5 equipos por partidos
        top_partidos = df_stats.nlargest(10, 'partidos')
        fig_top.add_trace(go.Bar(
            name='Partidos Jugados',
            x=top_partidos['equipo'],
            y=top_partidos['partidos'],
            text=top_partidos['partidos'],
            textposition='auto',
            marker_color='#2085ec'
        ))
        
        fig_top.update_layout(
            title="Top 10 Equipos por Partidos Jugados",
            xaxis_title="Equipo",
            yaxis_title="Número de Partidos",
            showlegend=False,
            height=400
            
        )
        
        st.plotly_chart(fig_top, use_container_width=False)