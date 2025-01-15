import pandas as pd
import numpy as np
import streamlit as st

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