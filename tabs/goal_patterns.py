import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
def show(df):
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