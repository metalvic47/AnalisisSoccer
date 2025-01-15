import streamlit as st
import plotly.graph_objects as go

def show(df, df_countries, df_shootouts):
    st.header("🌎 Comparativa de Continentes")
    
    # Crear un diccionario de países por continente
    continentes = df_countries.groupby(df_countries.columns[1])[df_countries.columns[0]].agg(list).to_dict()
    
    # Selector de continentes con valores por defecto
    col1, col2 = st.columns(2)
    with col1:
        continente1 = st.selectbox(
            "Selecciona el primer continente",
            options=sorted(continentes.keys()),
            index=sorted(continentes.keys()).index("Sudamérica"),  # Valor por defecto: Sudamerica
            key="cont1"
        )
    with col2:
        # Filtrar el segundo continente para no poder seleccionar el mismo
        continentes_disponibles = [c for c in continentes.keys() if c != continente1]
        default_index = continentes_disponibles.index("Europa") if "Europa" in continentes_disponibles else 0
        continente2 = st.selectbox(
            "Selecciona el segundo continente",
            options=sorted(continentes_disponibles),
            index=default_index,  # Valor por defecto: Europa
            key="cont2"
        )
    
    # Obtener países de los continentes seleccionados
    paises_cont1 = set(continentes[continente1])
    paises_cont2 = set(continentes[continente2])
    
    # Filtrar torneos por continente
    torneos_cont1 = df[df['home_team'].isin(paises_cont1)]['tournament'].unique()
    torneos_cont2 = df[df['home_team'].isin(paises_cont2)]['tournament'].unique()
    
    # Encontrar torneos comunes y específicos
    torneos_comunes = sorted(set(torneos_cont1) & set(torneos_cont2))
    
    # Selector de torneo con valor por defecto para FIFA World Cup qualification
    default_torneo_index = torneos_comunes.index("FIFA World Cup qualification") if "FIFA World Cup qualification" in torneos_comunes else 0
    torneo = st.selectbox(
        "Selecciona el torneo a comparar",
        options=torneos_comunes,
        index=default_torneo_index,
        key="torneo"
    )
    
    if torneo:
        # Filtrar datos por torneo y continentes
        df_torneo = df[df['tournament'] == torneo]
        
        # Crear métricas y visualizaciones
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.subheader(f"Estadísticas {continente1}")
            partidos_cont1 = df_torneo[
                (df_torneo['home_team'].isin(paises_cont1)) | 
                (df_torneo['away_team'].isin(paises_cont1))
            ]
            mostrar_estadisticas(partidos_cont1, paises_cont1)
            
        with col_stats2:
            st.subheader(f"Estadísticas {continente2}")
            partidos_cont2 = df_torneo[
                (df_torneo['home_team'].isin(paises_cont2)) | 
                (df_torneo['away_team'].isin(paises_cont2))
            ]
            mostrar_estadisticas(partidos_cont2, paises_cont2)
            
        # Gráfico comparativo
        mostrar_comparativa(partidos_cont1, partidos_cont2, continente1, continente2)
            # Después de los gráficos de pastel:
        mostrar_estadisticas_generales(df, paises_cont1, paises_cont2, continente1, continente2, df_shootouts)
        analizar_penaltis(df_shootouts, paises_cont1, paises_cont2, continente1, continente2)

def mostrar_estadisticas(df_partidos, paises):
    total_partidos = len(df_partidos)
    if total_partidos > 0:
        # Calcular victorias como local
        victorias_local = sum(
            (df_partidos['home_team'].isin(paises)) & 
            (df_partidos['home_score'] > df_partidos['away_score'])
        )
        
        # Calcular victorias como visitante
        victorias_visitante = sum(
            (df_partidos['away_team'].isin(paises)) & 
            (df_partidos['away_score'] > df_partidos['home_score'])
        )
        
        # Calcular empates
        empates = sum(df_partidos['home_score'] == df_partidos['away_score'])
        
        # Métricas
        st.metric("Victorias como Local", victorias_local)
        st.metric("Victorias como Visitante", victorias_visitante)
        st.metric("Empates", empates)
        
        # Calcular promedio de goles
        goles_favor = sum(
            df_partidos[df_partidos['home_team'].isin(paises)]['home_score']
        ) + sum(
            df_partidos[df_partidos['away_team'].isin(paises)]['away_score']
        )
        
        st.metric("Promedio de Goles por Partido", f"{goles_favor/total_partidos:.2f}")
    else:
        st.warning("No hay datos disponibles para el período seleccionado")

def mostrar_comparativa(df_cont1, df_cont2, continente1, continente2):
    st.subheader("Comparativa de Rendimiento")
    
    # Crear gráficos de pastel para cada continente
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico para el primer continente
        fig_cont1 = go.Figure()
        total_cont1 = len(df_cont1)
        
        if total_cont1 > 0:
            victorias_local_1 = sum((df_cont1['home_team'].isin(set(df_cont1['home_team']))) & 
                                  (df_cont1['home_score'] > df_cont1['away_score']))
            victorias_visit_1 = sum((df_cont1['away_team'].isin(set(df_cont1['home_team']))) & 
                                  (df_cont1['away_score'] > df_cont1['home_score']))
            empates_1 = sum(df_cont1['home_score'] == df_cont1['away_score'])
            
            valores_1 = [victorias_local_1, victorias_visit_1, empates_1]
            porcentajes_1 = [v/total_cont1*100 for v in valores_1]
            
            fig_cont1.add_trace(go.Pie(
                labels=['Victorias Local', 'Victorias Visitante', 'Empates'],
                values=porcentajes_1,
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>" +
                            "Porcentaje: %{percent}<br>" +
                            "Cantidad: %{value:.0f}<br>"
            ))
            
            fig_cont1.update_layout(
                title=f"Distribución de Resultados - {continente1}",
                height=400
            )
            
            st.plotly_chart(fig_cont1, use_container_width=True)
    
    with col2:
        # Gráfico para el segundo continente
        fig_cont2 = go.Figure()
        total_cont2 = len(df_cont2)
        
        if total_cont2 > 0:
            victorias_local_2 = sum((df_cont2['home_team'].isin(set(df_cont2['home_team']))) & 
                                  (df_cont2['home_score'] > df_cont2['away_score']))
            victorias_visit_2 = sum((df_cont2['away_team'].isin(set(df_cont2['home_team']))) & 
                                  (df_cont2['away_score'] > df_cont2['home_score']))
            empates_2 = sum(df_cont2['home_score'] == df_cont2['away_score'])
            
            valores_2 = [victorias_local_2, victorias_visit_2, empates_2]
            porcentajes_2 = [v/total_cont2*100 for v in valores_2]
            
            fig_cont2.add_trace(go.Pie(
                labels=['Victorias Local', 'Victorias Visitante', 'Empates'],
                values=porcentajes_2,
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>" +
                            "Porcentaje: %{percent}<br>" +
                            "Cantidad: %{value:.0f}<br>"
            ))
            
            fig_cont2.update_layout(
                title=f"Distribución de Resultados - {continente2}",
                height=400
            )
            
            st.plotly_chart(fig_cont2, use_container_width=True)

def mostrar_estadisticas_generales(df, paises_cont1, paises_cont2, continente1, continente2, df_shootouts):
    st.subheader("Estadísticas Generales por Continente")
    
    # Crear columnas para cada continente
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"### {continente1}")
        # Filtrar partidos del primer continente
        partidos_cont1 = df[
            (df['home_team'].isin(paises_cont1)) | 
            (df['away_team'].isin(paises_cont1))
        ]
        total_partidos1 = len(partidos_cont1)
        
        if total_partidos1 > 0:
            # Calcular estadísticas
            victorias_local = sum((partidos_cont1['home_team'].isin(paises_cont1)) & 
                                (partidos_cont1['home_score'] > partidos_cont1['away_score']))
            victorias_visita = sum((partidos_cont1['away_team'].isin(paises_cont1)) & 
                                 (partidos_cont1['away_score'] > partidos_cont1['home_score']))
            empates = sum(partidos_cont1['home_score'] == partidos_cont1['away_score'])
            
            # Mostrar porcentajes
            st.write(f"Victorias como Local: {(victorias_local/total_partidos1*100):.1f}%")
            st.write(f"Victorias como Visitante: {(victorias_visita/total_partidos1*100):.1f}%")
            st.write(f"Empates: {(empates/total_partidos1*100):.1f}%")
    
    with col2:
        st.write(f"### {continente2}")
        # Filtrar partidos del segundo continente
        partidos_cont2 = df[
            (df['home_team'].isin(paises_cont2)) | 
            (df['away_team'].isin(paises_cont2))
        ]
        total_partidos2 = len(partidos_cont2)
        
        if total_partidos2 > 0:
            # Calcular estadísticas
            victorias_local = sum((partidos_cont2['home_team'].isin(paises_cont2)) & 
                                (partidos_cont2['home_score'] > partidos_cont2['away_score']))
            victorias_visita = sum((partidos_cont2['away_team'].isin(paises_cont2)) & 
                                 (partidos_cont2['away_score'] > partidos_cont2['home_score']))
            empates = sum(partidos_cont2['home_score'] == partidos_cont2['away_score'])
            
            # Mostrar porcentajes
            st.write(f"Victorias como Local: {(victorias_local/total_partidos2*100):.1f}%")
            st.write(f"Victorias como Visitante: {(victorias_visita/total_partidos2*100):.1f}%")
            st.write(f"Empates: {(empates/total_partidos2*100):.1f}%")

def analizar_penaltis(df_shootouts, paises_cont1, paises_cont2, continente1, continente2):
    st.subheader("Análisis de Penaltis")
    
    # Filtrar penaltis por continente
    penaltis_cont1 = df_shootouts[
        (df_shootouts['home_team'].isin(paises_cont1)) | 
        (df_shootouts['away_team'].isin(paises_cont1))
    ]
    penaltis_cont2 = df_shootouts[
        (df_shootouts['home_team'].isin(paises_cont2)) | 
        (df_shootouts['away_team'].isin(paises_cont2))
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"### {continente1}")
        if len(penaltis_cont1) > 0:
            # Analizar resultados cuando tira primero
            primero_gana = sum(penaltis_cont1['first_shooter'] == penaltis_cont1['winner'])
            total_penaltis = len(penaltis_cont1)
            
            st.write(f"Cuando tira primero:")
            st.write(f"- Gana: {(primero_gana/total_penaltis*100):.1f}%")
            st.write(f"- Pierde: {((total_penaltis-primero_gana)/total_penaltis*100):.1f}%")
    
    with col2:
        st.write(f"### {continente2}")
        if len(penaltis_cont2) > 0:
            # Analizar resultados cuando tira primero
            primero_gana = sum(penaltis_cont2['first_shooter'] == penaltis_cont2['winner'])
            total_penaltis = len(penaltis_cont2)
            
            st.write(f"Cuando tira primero:")
            st.write(f"- Gana: {(primero_gana/total_penaltis*100):.1f}%")
            st.write(f"- Pierde: {((total_penaltis-primero_gana)/total_penaltis*100):.1f}%")