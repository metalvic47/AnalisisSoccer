import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def show(df):
    st.header("🏆 Comparativa de Torneos")
    
   
    # Selector de torneos
    selected_tournaments = st.multiselect(
        "Selecciona torneos para comparar",
        df['tournament'].unique(),
        default=['FIFA World Cup', 'UEFA Euro', 'Copa América']
    )
    
    if selected_tournaments:
        tournament_data = df[df['tournament'].isin(selected_tournaments)]
        
        # Análisis general por torneo
        st.subheader("📊 Estadísticas por Torneo")
        
        # Calcular estadísticas por torneo
        tournament_stats = []
        for torneo in selected_tournaments:
            torneo_matches = tournament_data[tournament_data['tournament'] == torneo]
            
            # Estadísticas básicas
            total_matches = len(torneo_matches)
            avg_goals = (torneo_matches['home_score'] + torneo_matches['away_score']).mean()
            max_goals = (torneo_matches['home_score'] + torneo_matches['away_score']).max()
            clean_sheets = sum((torneo_matches['home_score'] == 0) | (torneo_matches['away_score'] == 0))
            
            tournament_stats.append({
                'Torneo': torneo,
                'Partidos': total_matches,
                'Promedio Goles': round(avg_goals, 2),
                'Máximo Goles': int(max_goals),
                'Porterías Imbatidas': clean_sheets,
                'Goles Totales': int(torneo_matches['home_score'].sum() + torneo_matches['away_score'].sum())
            })
        
        # Mostrar tabla de estadísticas
        st.dataframe(pd.DataFrame(tournament_stats).set_index('Torneo'))
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de promedio de goles
            fig_goals = px.bar(
                tournament_stats,
                x='Torneo',
                y='Promedio Goles',
                title="Promedio de Goles por Partido",
                text='Promedio Goles',
                color='Torneo',
                color_discrete_sequence=["#72b4eb", "#2085ec" ,"#cea9bc"]
                
            )
            fig_goals.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig_goals, use_container_width=True)
        with col2:
            # Distribución de goles
            fig_dist = go.Figure()
            colors = ["#72b4eb", "#2085ec" ,"#cea9bc"]  # Lista de colores

            for i, torneo in enumerate(selected_tournaments):
                torneo_data = tournament_data[tournament_data['tournament'] == torneo]
                goles_partido = torneo_data['home_score'] + torneo_data['away_score']
                
                fig_dist.add_trace(go.Box(
                    y=goles_partido,
                    name=torneo,
                    boxpoints='all',
                    jitter=0.3,
                    pointpos=-1.8,
                    marker_color=colors[i % len(colors)]  # Asignar color
                ))
            
            fig_dist.update_layout(
                title="Distribución de Goles por Partido",
                yaxis_title="Goles por Partido",
                showlegend=True
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        
        
        # Análisis de tendencias temporales
        if 'year' not in tournament_data.columns:
            tournament_data['year'] = pd.to_datetime(tournament_data['date']).dt.year
            
        st.subheader("📈 Evolución Histórica")
        
        # Gráfico de evolución de goles
        fig_evolution = go.Figure()
        
        for torneo in selected_tournaments:
            torneo_data = tournament_data[tournament_data['tournament'] == torneo]
            yearly_goals = torneo_data.groupby('year').agg({
                'home_score': 'sum',
                'away_score': 'sum'
            }).reset_index()
            yearly_goals['total_goals'] = yearly_goals['home_score'] + yearly_goals['away_score']
            
            fig_evolution.add_trace(go.Scatter(
                x=yearly_goals['year'],
                y=yearly_goals['total_goals'],
                name=torneo,
                mode='lines+markers'
            ))
        
        fig_evolution.update_layout(
            title="Evolución de Goles Totales por Año",
            xaxis_title="Año",
            yaxis_title="Goles Totales",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_evolution, use_container_width=True)