import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show(df):
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

    # Métricas generales
    st.markdown("### 📊 Métricas Generales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_matches = len(df_filtered)
        st.metric("Total de Partidos", f"{total_matches:,}")
    
    with col2:
        avg_goals = (df_filtered['home_score'] + df_filtered['away_score']).mean()
        st.metric("Promedio de Goles por Partido", f"{avg_goals:.2f}")
    
    with col3:
        home_wins = (df_filtered['resultado'] == 'Victoria Local').mean() * 100
        st.metric("% Victorias Locales", f"{home_wins:.1f}%")
    
    with col4:
        most_common_score = f"{df_filtered['home_score'].mode().iloc[0]}-{df_filtered['away_score'].mode().iloc[0]}"
        st.metric("Resultado más Común", most_common_score)

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

    # Gráfico de número de partidos por año
    partidos_por_año = df_filtered.groupby('year').size()
    fig_partidos = go.Figure()

    fig_partidos.add_trace(
        go.Scatter(
            x=partidos_por_año.index,
            y=partidos_por_año.values,
            name='Total Partidos',
            mode='lines+markers',
            line=dict(color='#FFD700'),
            marker=dict(color='#FFD700'),
            hovertemplate="Año: %{x}<br>" +
                         "Partidos: %{y}<br>" +
                         "<extra></extra>"
        )
    )

    fig_partidos.update_layout(
        title="Evolución del Número Total de Partidos por Año",
        xaxis_title="Año",
        yaxis_title="Número de Partidos",
        hovermode='x unified',
        showlegend=True
    )

    st.plotly_chart(fig_partidos, use_container_width=True)