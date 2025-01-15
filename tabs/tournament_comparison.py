import streamlit as st
import plotly.graph_objects as go

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