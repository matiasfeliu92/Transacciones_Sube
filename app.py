import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
"""

df_tables = pd.read_sql(query, engine)
df_tables = df_tables[df_tables['table_name'].str.contains('SUBE')]

df_Transacciones_SUBE = pd.DataFrame()
for table in df_tables['table_name']:
    print(table)
    df = pd.read_sql(f'SELECT * FROM "public"."{table}"', engine)
    df_Transacciones_SUBE = pd.concat([df_Transacciones_SUBE, df], ignore_index=True)
engine.dispose()

st.set_page_config(layout="wide")

st.title('Reporte de transacciones de SUBE')

container_1 = st.container()

df_Transacciones_SUBE_periodo = df_Transacciones_SUBE.groupby('Periodo').size().reset_index(name='count').nlargest(10, 'count')
fig_1 = px.bar(df_Transacciones_SUBE_periodo, x='Periodo', y='count')

with container_1:
    st.header('¿En que periodos se registraron la mayor cantidad de transacciones de SUBE?')
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_Transacciones_SUBE_periodo, use_container_width=True)

    with col2:
        st.plotly_chart(fig_1, use_container_width=True)

container_2 = st.container()

df_Transacciones_SUBE_por_anio = df_Transacciones_SUBE.groupby('Anio').size().reset_index(name='count')
fig_2 = px.pie(df_Transacciones_SUBE_por_anio, values='count', names='Anio')

with container_2:
    st.header('¿En que año se registro la mayor cantidad de transacciones de SUBE?')
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_Transacciones_SUBE_por_anio, use_container_width=True)

    with col2:
        st.plotly_chart(fig_2, use_container_width=True)