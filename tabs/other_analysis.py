import streamlit as st
import plotly.express as px
import pandas as pd

def load_data(df, df_countries, df_goalscorers):
    """Carga y prepara los datos."""
    continentes = df_countries.groupby(df_countries.columns[1])[df_countries.columns[0]].agg(list).to_dict()
    
    # Convertir df_goalscorers a DataFrame
    columns = ['date', 'home_team', 'away_team', 'team', 'scorer', 'minute', 'own_goal', 'penalty']
    df_goalscorers = pd.DataFrame(df_goalscorers, columns=columns)
    df_goalscorers['date'] = pd.to_datetime(df_goalscorers['date'])
    df_goalscorers['year'] = df_goalscorers['date'].dt.year
    
    # Crear columna 'resultado' si no existe
    if 'resultado' not in df.columns:
        df['resultado'] = df.apply(lambda row: 
            'Victoria Local' if row['home_score'] > row['away_score']
            else 'Victoria Visitante' if row['home_score'] < row['away_score']
            else 'Empate', axis=1)
    
    return df, df_goalscorers, continentes

def filter_data(df_goalscorers, continentes):
    """Filtra los datos según el periodo de análisis y los continentes seleccionados."""
    min_year = df_goalscorers['year'].min()
    max_year = df_goalscorers['year'].max()
    selected_years = st.slider("Selecciona el periodo de análisis", min_year, max_year, (min_year, max_year))
    df_goalscorers = df_goalscorers[(df_goalscorers['year'] >= selected_years[0]) & (df_goalscorers['year'] <= selected_years[1])]

    default_continents = ["Sudamérica", "Europa"]
    selected_continents = st.multiselect("Selecciona dos continentes para comparar", list(continentes.keys()), default=default_continents)

    if len(selected_continents) != 2:
        st.error("Por favor selecciona exactamente dos continentes.")
        return None, None, None, None

    continent1, continent2 = selected_continents
    countries_cont1 = continentes[continent1]
    countries_cont2 = continentes[continent2]

    df_cont1 = df_goalscorers[
        (df_goalscorers['home_team'].isin(countries_cont1)) |
        (df_goalscorers['away_team'].isin(countries_cont1))
    ]
    df_cont2 = df_goalscorers[
        (df_goalscorers['home_team'].isin(countries_cont2)) |
        (df_goalscorers['away_team'].isin(countries_cont2))
    ]
    
    return df_cont1, df_cont2, continent1, continent2

def analyze_first_goal(df, df_cont):
    """Analiza el primer gol de los partidos."""
    df_cont = df_cont.merge(df[['date', 'home_team', 'away_team', 'resultado']], on=['date', 'home_team', 'away_team'], how='left')
    df_cont['game_id'] = df_cont.groupby(['date', 'home_team', 'away_team']).ngroup()
    df_cont = df_cont.sort_values(by=['game_id', 'minute'])

    first_goal = df_cont.groupby('game_id').first().reset_index()
    first_goal['won'] = first_goal.apply(
        lambda row: 'Ganado' if (row['team'] == row['home_team'] and row['resultado'] == 'Victoria Local') 
        or (row['team'] == row['away_team'] and row['resultado'] == 'Victoria Visitante') 
        else 'Perdido', axis=1
    )
    first_goal['home_or_away'] = first_goal.apply(lambda row: 'Local' if row['team'] == row['home_team'] else 'Visitante', axis=1)
    
    home_wins = first_goal[first_goal['home_or_away'] == 'Local']['won'].value_counts(normalize=True).mul(100).round(2).reset_index()
    home_wins.columns = ['Resultado', 'Porcentaje']
    away_wins = first_goal[first_goal['home_or_away'] == 'Visitante']['won'].value_counts(normalize=True).mul(100).round(2).reset_index()
    away_wins.columns = ['Resultado', 'Porcentaje']
    
    return home_wins, away_wins

def create_donut_chart(df, title):
    """Crea gráficos de dona."""
    fig = px.pie(df, names='Resultado', values='Porcentaje', hole=0.4,
                 color='Resultado', color_discrete_map={'Ganado': 'blue', 'Perdido': 'red'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title=title, title_x=0.5)
    return fig

def show_visualization(home_wins_cont1, away_wins_cont1, home_wins_cont2, away_wins_cont2, continent1, continent2):
    """Muestra los gráficos en Streamlit."""
    st.subheader(f"Análisis de Ventaja al Marcar el Primer Gol ({continent1} vs. {continent2})")
    st.write("Este análisis muestra si los equipos locales y visitantes tienen ventaja al marcar el primer gol en un partido.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {continent1}")
        col1_1, col1_2 = st.columns([1, 1])
        
        with col1_1:
            st.markdown("#### Equipos Locales")
            fig1 = create_donut_chart(home_wins_cont1, "Equipos Locales")
            st.plotly_chart(fig1)
        with col1_2:
            st.markdown("#### Equipos Visitantes")
            fig2 = create_donut_chart(away_wins_cont1, "Equipos Visitantes")
            st.plotly_chart(fig2)

    with col2:
        st.markdown(f"### {continent2}")
        col2_1, col2_2 = st.columns([1, 1])
        with col2_1:
            st.markdown("#### Equipos Locales")
            fig3 = create_donut_chart(home_wins_cont2, "Equipos Locales")
            st.plotly_chart(fig3)
        with col2_2:
            st.markdown("#### Equipos Visitantes")
            fig4 = create_donut_chart(away_wins_cont2, "Equipos Visitantes")
            st.plotly_chart(fig4)

def show(df, df_countries, df_goalscorers):
    df, df_goalscorers, continentes = load_data(df, df_countries, df_goalscorers)
    df_cont1, df_cont2, continent1, continent2 = filter_data(df_goalscorers, continentes)

    if df_cont1 is not None and df_cont2 is not None:
        home_wins_cont1, away_wins_cont1 = analyze_first_goal(df, df_cont1)
        home_wins_cont2, away_wins_cont2 = analyze_first_goal(df, df_cont2)
        show_visualization(home_wins_cont1, away_wins_cont1, home_wins_cont2, away_wins_cont2, continent1, continent2)
    analyze_team(df, df_goalscorers)
    #analyze_penalty_goals(df,df_goalscorers)


def analyze_team(df, df_goalscorers):
    """Realiza el análisis de un equipo seleccionado."""
    teams = df_goalscorers['team'].unique().tolist()
    default_team = "Ecuador"
    selected_team = st.selectbox("Selecciona un equipo para el análisis", teams, index=teams.index(default_team))

    df_team = df_goalscorers[
        (df_goalscorers['home_team'] == selected_team) | 
        (df_goalscorers['away_team'] == selected_team)
    ]

    if df_team.empty:
        st.warning(f"No hay datos disponibles para el equipo: {selected_team}")
        return

    home_wins, away_wins = analyze_first_goal(df, df_team)
    st.subheader(f"Análisis de Ventaja al Marcar el Primer Gol - Equipo {selected_team}")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Equipos Locales")
        fig1 = create_donut_chart(home_wins, "Equipos Locales")
        st.plotly_chart(fig1)
    
    with col2:
        st.markdown("#### Equipos Visitantes")
        fig2 = create_donut_chart(away_wins, "Equipos Visitantes")
        st.plotly_chart(fig2)
#def analyze_penalty_goals(df, df_goalscorers):
    """Realiza el análisis del primer gol cuando es convertido de penal."""
    penalty_goals = df_goalscorers[df_goalscorers['penalty'] == True]
    if penalty_goals.empty:
        st.warning("No hay datos disponibles para goles de penal")